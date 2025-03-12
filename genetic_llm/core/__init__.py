from typing import NamedTuple
from pydantic import BaseModel, Field, ConfigDict
from genetic_llm.core_abc import GeneticConfigABC, AgentABC
from genetic_llm.core_abc.chromosome_type import ChromosomeType
import random

def tournament_selection(population: list[Agent]) -> list[Agent]:
    """Select top 25% performers"""
    k = max(2, len(population) // 4)
    return sorted(population, key=lambda a: a.fitness, reverse=True)[:k]

def single_point_crossover(parent1: Agent, parent2: Agent) -> Agent:
    """Combine task chromosomes from both parents"""
    t1 = next(c for c in parent1.chromosomes if c.type == ChromosomeType.TASK).value
    t2 = next(c for c in parent2.chromosomes if c.type == ChromosomeType.TASK).value
    crossover_point = len(t1) // 2
    return Agent((
        Chromosome(ChromosomeType.TASK, t1[:crossover_point] + t2[crossover_point:]),
        parent1.chromosomes[1],
        parent1.chromosomes[2],
    ))


class GeneticConfig(BaseModel, GeneticConfigABC):
    model_config = ConfigDict(validate_default=True)
    population_size: int = Field(default=50, gt=0)
    mutation_rate: float = Field(default=0.05, ge=0.0, le=1.0)
    elite_size: int = Field(default=5, ge=0)
    max_length: int = Field(default=23)
    fitness_weights: dict = Field(default={"a_score": 1.0, "length_penalty": -1.0})

class Chromosome(NamedTuple):
    type: ChromosomeType
    value: str

    def __new__(cls, chrom_type: ChromosomeType, value: str):
        if not isinstance(chrom_type, ChromosomeType):
            raise TypeError(f"Invalid chromosome type {chrom_type.__class__.__name__}")
        return super().__new__(cls, chrom_type, value)


class Agent(AgentABC):
    def __init__(self, chromosomes: tuple[Chromosome, ...], fitness: float = 0.0):  # pylint: disable=too-many-locals
        required_types = {ChromosomeType.TASK, ChromosomeType.MATE_SELECTION, ChromosomeType.RECOMBINATION}
        seen_types = set()

        # Validate chromosome types and uniqueness
        for chromo in chromosomes:
            if not isinstance(chromo.type, ChromosomeType):
                raise TypeError(f"Invalid chromosome type {type(chromo.type)} - must be ChromosomeType")
            if chromo.type in seen_types:
                raise ValueError(f"Duplicate chromosome type: {chromo.type}")
            seen_types.add(chromo.type)

        # Check required types
        if not required_types.issubset(seen_types):
            missing = required_types - seen_types
            raise ValueError(f"Missing required chromosome types: {', '.join(mt.value for mt in missing)}")
            
        if not 0.0 <= fitness <= 1.0:
            raise ValueError(f"Invalid fitness {fitness:.2f} - must be between 0.0-1.0")  # Fitness normalized 0-1 for selection

        self.chromosomes = chromosomes
        self.fitness = fitness
        
    def __repr__(self) -> str:
        return f"Agent(fitness={self.fitness:.2f}, chromosomes={[c.type for c in self.chromosomes]})"
    
    # Implement abstract methods from AgentABC
    def select_mates(self, population: list['Agent']) -> list['Agent']:
        selector_name = next(c.value for c in self.chromosomes 
                          if c.type == ChromosomeType.MATE_SELECTION)
        return globals()[selector_name](population, self)

    def recombine(self, partner: 'Agent') -> 'Agent':
        recombinator_name = next(c.value for c in self.chromosomes
                              if c.type == ChromosomeType.RECOMBINATION)
        return globals()[recombinator_name](self, partner)

