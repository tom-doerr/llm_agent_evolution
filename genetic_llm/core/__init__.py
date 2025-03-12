from typing import NamedTuple
from pydantic import BaseModel, Field, ConfigDict
from genetic_llm.core_abc import GeneticConfigABC, AgentABC
from genetic_llm.core_abc.chromosome_type import ChromosomeType
from genetic_llm.core_abc.chromosome_type import ChromosomeType


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
    def __init__(self, chromosomes: tuple[Chromosome, ...], fitness: float = 0.0):
        required_types = {ChromosomeType.TASK, ChromosomeType.MATE_SELECTION, ChromosomeType.RECOMBINATION}
        seen_types = set()
        
        for c in chromosomes:
            if not isinstance(c.type, ChromosomeType):
                raise TypeError(f"Invalid chromosome type {type(c.type)} - must be ChromosomeType")
            if c.type in seen_types:
                raise ValueError(f"Duplicate chromosome type: {c.type}")
            seen_types.add(c.type)
        
        missing = required_types - seen_types
        if missing:
            raise ValueError(f"Missing required chromosome types: {', '.join(mt.value for mt in missing)}")
            
        if not 0.0 <= fitness <= 1.0:
            raise ValueError(f"Invalid fitness {fitness:.2f} - must be between 0.0-1.0")

        self.chromosomes = chromosomes
        self.fitness = fitness
        
    def __repr__(self) -> str:
        return f"Agent(fitness={self.fitness:.2f}, chromosomes={[c.type for c in self.chromosomes]})"
    
    # Implement abstract methods from AgentABC
    def select_mates(self, population: list[Agent]) -> list[Agent]:
        """Select mating partners from population"""
        # Implementation left as placeholder since mate selection logic
        # should be in the corresponding chromosome
        return []

    def recombine(self, partner: Agent) -> Agent:
        """Recombine with partner agent to produce new offspring"""
        # Implementation left as placeholder since recombination logic
        # should be in the corresponding chromosome
        return self

