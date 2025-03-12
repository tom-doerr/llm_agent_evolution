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
        for ct, value in chromosomes.items():
            if ct not in self.schemas:
                raise ValueError(f"No schema defined for chromosome type {ct}")
            try:
                parsed = json.loads(value)
                validate(instance=parsed, schema=self.schemas[ct])
            except (json.JSONDecodeError, ValidationError) as e:
                raise ValueError(f"Invalid {ct} chromosome: {str(e)}") from e
        return True
