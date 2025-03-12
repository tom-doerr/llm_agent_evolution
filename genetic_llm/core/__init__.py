from enum import Enum
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Dict, List

class ChromosomeType(Enum):
    TASK = "task"
    MATE_SELECTION = "mate_selection"
    RECOMBINATION = "recombination"

class GeneticConfig(BaseModel):
    population_size: int = 50
    mutation_rate: float = 0.05
    elite_size: int = 5

class Agent:
    def __init__(self, chromosomes: Dict[ChromosomeType, str]):
        self.chromosomes = chromosomes
        self.fitness: float = 0.0

# Interface contracts
class MateSelector(ABC):
    @abstractmethod
    def select(self, population: List['Agent']) -> 'Agent':
        """Select a mate from population based on strategy"""
        
class RecombinerABC(ABC):
    @abstractmethod
    def combine(self, parent1: str, parent2: str) -> str:
        """Combine two chromosome strings into new offspring"""
