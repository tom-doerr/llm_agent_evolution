from typing import Dict
import json
from jsonschema import validate, ValidationError
from abc import ABC, abstractmethod

class ChromosomeValidatorABC(ABC):
    @abstractmethod
    def validate(self, chromosomes: Dict[str, str]) -> bool:
        """Validate chromosome structure against schema"""

class JSONSchemaValidator(ChromosomeValidatorABC):
    def __init__(self, schemas: Dict[str, dict]):
        self.schemas = schemas
        
    def validate(self, chromosomes: Dict[str, str]) -> bool:
        for chromosome_type, json_str in chromosomes.items():
            schema = self.schemas.get(chromosome_type)
            if not schema:
                raise ValueError(f"No schema defined for chromosome type {chromosome_type}")
            
            try:
                data = json.loads(json_str)
                validate(instance=data, schema=schema)
            except (json.JSONDecodeError, ValidationError) as e:
                raise ValueError(f"Invalid {chromosome_type} chromosome: {str(e)}") from e
        return True
