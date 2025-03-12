from enum import Enum
from pydantic import BaseModel, Field, ValidationError
from abc import ABC, abstractmethod
from typing import Dict, List, NamedTuple

class ChromosomeType(Enum):
    TASK = "task"
    MATE_SELECTION = "mate_selection"
    RECOMBINATION = "recombination"

class GeneticConfig(BaseModel):
    population_size: int = Field(default=50, gt=0)
    mutation_rate: float = Field(default=0.05, ge=0.0, le=1.0)
    elite_size: int = Field(default=5, ge=0)

class Chromosome(NamedTuple):
    type: ChromosomeType
    value: str

from ..core_abc import AgentABC

class Agent(AgentABC):
    def __init__(self, chromosomes: tuple[Chromosome, ...], fitness: float = 0.0):
        # Validate chromosome types
        if not chromosomes:
            raise ValueError("At least one chromosome required")
            
        seen_types = set()
        for c in chromosomes:
            if not isinstance(c.type, ChromosomeType):
                raise TypeError(f"Invalid chromosome type {type(c.type)} - must be ChromosomeType")
            if c.type in seen_types:
                raise ValueError(f"Duplicate chromosome type: {c.type}")
            seen_types.add(c.type)
            
        # Validate fitness range
        if not 0.0 <= fitness <= 1.0:
            raise ValueError(f"Invalid fitness {fitness:.2f} - must be between 0.0-1.0")

        # Store chromosomes as type:value mapping
        self.chromosomes = {c.type: c.value for c in chromosomes}
        self.fitness = fitness
        
    def __repr__(self) -> str:
        return f"Agent(fitness={self.fitness:.2f}, chromosomes={list(self.chromosomes.keys())})"

