"""Natural language layer: free-text question -> query function call via Claude.

Claude never writes SQL (DESIGN.md D4). It picks one of the four vetted query
functions and fills in its arguments; this module runs the real function and
sends the rows back for a final natural-language answer.

The system prompt is built from registry.describe_ontology(), so the model
reads the live ontology instead of a hardcoded schema description.

Requires ANTHROPIC_API_KEY in .env.
"""
from datetime import date

import anthropic
from dotenv import load_dotenv

from purdo.db import get_session
from purdo.ontology.registry import describe_ontology
from purdo.queries import core

load_dotenv()

MODEL = "claude-haiku-4-5"

TOOLS = [
    {
        "name": "unsatisfied_requirements",
        "description": (
            "List degree requirements the student has NOT yet finished, with credits "
            "earned, credits needed, and the remaining gap. Use for questions like "
            "'what am I missing for graduation', 'what requirements do I still need', "
            "or 'how many credits short am I'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "blocked_courses",
        "description": (
            "List planned courses that cannot be taken yet because at least one "
            "prerequisite is not completed, naming the missing prerequisite. Use for "
            "questions like 'what can't I take yet', 'am I blocked from anything', or "
            "'which prereqs am I missing'. An empty result means nothing is blocked."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "due_this_week",
        "description": (
            "List assignments still to do in the seven days after a given date, with "
            "course code and due date. Use for questions like 'what's due this week' "
            "or 'what homework do I have coming up'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "today": {
                    "type": "string",
                    "description": "Start of the window as YYYY-MM-DD. Omit to use the real today.",
                },
            },
            "required": [],
        },
    },
    {
        "name": "upcoming_exams",
        "description": (
            "List exams within a number of days after a given date, with course code "
            "and exam date. Use for questions like 'when are my midterms' or 'do I "
            "have any exams coming up'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "today": {
                    "type": "string",
                    "description": "Start of the window as YYYY-MM-DD. Omit to use the real today.",
                },
                "days": {
                    "type": "integer",
                    "description": "How many days ahead to look. Defaults to 28.",
                },
            },
            "required": [],
        },
    },
]


def run_tool(session, name, args):
    """Execute the query function Claude chose. This is the only dispatch point."""
    today = date.fromisoformat(args["today"]) if args.get("today") else date.today()

    if name == "unsatisfied_requirements":
        return core.unsatisfied_requirements(session)
    if name == "blocked_courses":
        return core.blocked_courses(session)
    if name == "due_this_week":
        return core.due_this_week(session, today)
    if name == "upcoming_exams":
        return core.upcoming_exams(session, today, args.get("days", 28))
    raise ValueError(f"unknown tool: {name}")


def build_system_prompt(session):
    return (
        "You are Purdo, an academic planning assistant for one Purdue CS student.\n"
        "Answer questions about their degree progress using ONLY the tools provided — "
        "never guess at data and never write SQL.\n"
        "After a tool returns, answer in two or three plain sentences. Name specific "
        "courses, credit counts, and dates from the data. If a tool returns an empty "
        "list, say plainly that there is nothing in that category.\n\n"
        "The data follows this ontology:\n\n" + describe_ontology(session)
    )


def ask(question, session=None):
    """Answer a natural-language question. Returns answer, tool used, and raw rows."""
    own_session = session is None
    session = session or get_session()
    client = anthropic.Anthropic()

    messages = [{"role": "user", "content": question}]
    tool_used, data = None, None

    try:
        while True:
            response = client.messages.create(
                model=MODEL,
                max_tokens=2000,
                system=build_system_prompt(session),
                tools=TOOLS,
                messages=messages,
            )

            if response.stop_reason != "tool_use":
                answer = "".join(b.text for b in response.content if b.type == "text")
                return {"answer": answer, "tool_used": tool_used, "data": data}

            messages.append({"role": "assistant", "content": response.content})

            results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                tool_used, data = block.name, run_tool(session, block.name, block.input)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(data),
                })
            messages.append({"role": "user", "content": results})
    finally:
        if own_session:
            session.close()


if __name__ == "__main__":
    import sys

    q = " ".join(sys.argv[1:]) or "What am I missing for graduation?"
    result = ask(q)
    print(f"Q: {q}")
    print(f"[tool: {result['tool_used']}]")
    print(result["answer"])
