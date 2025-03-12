from enum import Enum
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Dict, List, NamedTuple

class ChromosomeType(Enum):
    TASK = "task"
    MATE_SELECTION = "mate_selection"
    RECOMBINATION = "recombination"

class GeneticConfig(BaseModel):
    population_size: int = 50
    mutation_rate: float = 0.05
    elite_size: int = 5

class Chromosome(NamedTuple):
    type: ChromosomeType
    value: str

class Agent:
    """Represents an evolutionary agent with genetic programming components."""
    def __init__(self, chromosomes: tuple[Chromosome, ...], fitness: float = 0.0):
        self.chromosomes = {c.type: c.value for c in chromosomes}
        self.fitness = fitness
        
    def __repr__(self) -> str:
        """Provide clear string representation for debugging."""
        return f"Agent(fitness={self.fitness:.2f}, chromosomes={self.chromosomes.keys()})"

