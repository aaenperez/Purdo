"""Natural language layer: free-text question -> query function call via Claude.

YOU WRITE THIS (Lesson 11). Spec:
- Tool definitions mapping 1:1 to the functions in purdo.queries.core
  (name, description, JSON-schema input like `days`).
- System prompt built from registry.describe_ontology() — the model reads the
  live ontology, nothing hardcoded.
- ask(question: str) -> {"answer": str, "tool_used": str, "data": ...}:
  one Claude call with tools; execute the chosen tool; send the result back for
  a final natural-language answer. The model NEVER writes SQL (DESIGN.md D4).
- Requires ANTHROPIC_API_KEY in .env.
"""
