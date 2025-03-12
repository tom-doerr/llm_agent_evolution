from enum import Enum
from pydantic import BaseModel

class ChromosomeType(Enum):
    TASK = "task"
    MATE_SELECTION = "mate_selection"
    RECOMBINATION = "recombination"

class GeneticConfig(BaseModel):
    population_size: int = 50
    mutation_rate: float = 0.05
    elite_size: int = 5

class Agent:
    def __init__(self, chromosomes: dict[ChromosomeType, str]):
        self.chromosomes = chromosomes
        self.fitness: float = 0.0
