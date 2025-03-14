from genetic_llm.core import ChromosomeType

DEFAULT_SCHEMAS = {
    "DNA": {  # Using string keys until enum values are confirmed
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "sequence": {"type": "string", "pattern": "^[ACGT]+$"},
            "length": {"type": "integer", "minimum": 1}
        },
        "required": ["sequence", "length"],
        "additionalProperties": False
    },
    "PROMPT": {  # Using string keys until enum values are confirmed
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "text": {"type": "string", "minLength": 10},
            "variables": {
                "type": "array",
                "items": {"type": "string"},
                "uniqueItems": True
            }
        },
        "required": ["text"],
        "additionalProperties": False
    },
    "MODEL_CONFIG": {  # Using string keys until enum values are confirmed
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "model_type": {"type": "string", "enum": ["llama", "gpt", "gemini"]},
            "temperature": {"type": "number", "minimum": 0, "maximum": 2}
        },
        "required": ["model_type"],
        "additionalProperties": False
    }
}
