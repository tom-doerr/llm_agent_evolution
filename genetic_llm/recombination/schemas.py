from jsonschema import validate, ValidationError

CHROMOSOME_SCHEMA = {
    "type": "object",
    "properties": {
        "genes": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        },
        "metadata": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "enum": ["cross", "mutation"]}
            }
        }
    },
    "required": ["genes"],
    "additionalProperties": False
}

def validate_chromosome(data: str) -> bool:
    """Validates chromosome structure against schema. Returns True if valid."""
    try:
        import json
        parsed = json.loads(data)
        validate(instance=parsed, schema=CHROMOSOME_SCHEMA)
        return True
    except (ValidationError, json.JSONDecodeError):
        return False
