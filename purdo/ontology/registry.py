"""The ontology registry: object types and link types as queryable metadata.

YOU WRITE THIS (Lesson 4). Spec:
- ObjectType(name, table_name, description)
- LinkType(name, source_type, target_type, table_name, description,
  properties_json)  # e.g. ENROLLED_IN carries ["status", "grade"]
- A register_ontology(session) function that populates both tables from the
  models in models.py.
- describe_ontology(session) -> str: a human/LLM-readable summary of the whole
  ontology. This string later becomes part of the Claude system prompt.
"""
