from typing import NamedTuple
from pydantic import BaseModel, Field, ConfigDict
from genetic_llm.core_abc import GeneticConfigABC, AgentABC, PopulationEvaluatorABC
from genetic_llm.core_abc.chromosome_type import ChromosomeType
import random

class GeneticConfig(BaseModel, GeneticConfigABC):
    model_config = ConfigDict(validate_default=True)
    population_size: int = Field(default=50, gt=0)
    mutation_rate: float = Field(default=0.05, ge=0.0, le=1.0)
    elite_size: int = Field(default=5, ge=0)
    max_length: int = Field(default=23)
    fitness_weights: dict = Field(default={"a_score": 1.0, "length_penalty": -1.0})
    
    @model_validator(mode='after')
    def check_fitness_weights(self):
        required_keys = {'a_score', 'length_penalty'}
        if not required_keys.issubset(self.fitness_weights):
            missing = required_keys - self.fitness_weights.keys()
            raise ValueError(f"Missing fitness weights: {missing}")
        return self

class Chromosome(NamedTuple):
    type: ChromosomeType
    value: str

    def __new__(cls, chrom_type: ChromosomeType, value: str):
        if not isinstance(chrom_type, ChromosomeType):
            raise TypeError(f"Invalid chromosome type {chrom_type.__class__.__name__}")
        return super().__new__(cls, chrom_type, value)



def tournament_selection(population: list[Agent], agent: Agent) -> list[Agent]:
    """Select top 25% performers (ignoring agent parameter)"""
    k = max(2, len(population) // 4)
    return sorted(population, key=lambda a: a.fitness, reverse=True)[:k]

def single_point_crossover(parent1: Agent, parent2: Agent) -> Agent:
    """Combine task chromosomes from both parents"""
    t1 = next(c for c in parent1.chromosomes if c.type == ChromosomeType.TASK).value
    t2 = next(c for c in parent2.chromosomes if c.type == ChromosomeType.TASK).value
    crossover_point = len(t1) // 2
    return Agent((  # pylint: disable=abstract-class-instantiated
        Chromosome(ChromosomeType.TASK, t1[:crossover_point] + t2[crossover_point:]),
        parent1.chromosomes[1],
        parent1.chromosomes[2],
    ))

class Agent(AgentABC):
    def __init__(self, chromosomes: tuple[Chromosome, ...], fitness: float = 0.0):
        self._validate_chromosomes(chromosomes)
            
        if not 0.0 <= fitness <= 1.0:
            raise ValueError(f"Invalid fitness {fitness:.2f} - must be between 0.0-1.0")

        self.chromosomes = chromosomes
        self.fitness = fitness
        
    def __repr__(self) -> str:
        return f"Agent(fitness={self.fitness:.2f}, chromosomes={[c.type for c in self.chromosomes]})"
    
    def select_mates(self, population: list['Agent']) -> list['Agent']:
        selector_name = next(c.value for c in self.chromosomes 
                          if c.type == ChromosomeType.MATE_SELECTION)
        return globals()[selector_name](population, self)

    def recombine(self, partner: 'Agent') -> 'Agent':
        recombinator_name = next(c.value for c in self.chromosomes
                              if c.type == ChromosomeType.RECOMBINATION)
        return globals()[recombinator_name](self, partner)

def evolve_population(population: list[Agent], config: GeneticConfig, evaluator: PopulationEvaluatorABC) -> list[Agent]:
    if not population:
        raise ValueError("Cannot evolve empty population")
    
    new_population = []
    
    # Preserve elites with safety check
    try:
        elites = sorted(population, key=lambda a: a.fitness, reverse=True)[:config.elite_size]
    except KeyError as e:
        raise RuntimeError("Population contains agents with invalid fitness values") from e
    new_population.extend(elites)
    
    # Breed remaining population
    while len(new_population) < config.population_size:
        parent1 = random.choice(elites if elites else population)
        mates = parent1.select_mates(population)
        
        if not mates:  # Handle empty selection
            mates = [random.choice(population)]
            
        parent2 = random.choice(mates)
        
        child = parent1.recombine(parent2)
        
        # Apply mutation to all chromosomes
        mutated = tuple(
            evaluator.mutate(c, config.mutation_rate)
            for c in child.chromosomes
        )
        new_population.append(Agent(mutated))  # pylint: disable=abstract-class-instantiated
    
    return new_population[:config.population_size]

