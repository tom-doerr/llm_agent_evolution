from genetic_llm.core_abc import PopulationEvaluatorABC
from genetic_llm.core import Agent, GeneticConfig, Chromosome, ChromosomeType
import random

class StringOptimizationEvaluator(PopulationEvaluatorABC):
    """Evaluates strings based on 'a' count and length constraints"""
    def __init__(self, config: GeneticConfig):
        self.config = config
        
    def evaluate(self, population: list[Agent]) -> None:  # pylint: disable=too-many-locals
        max_fitness = -float('inf')
        min_fitness = float('inf')
        
        # First pass: calculate raw fitness
        for agent in population:
            output = next(c.value for c in agent.chromosomes 
                        if c.type == ChromosomeType.TASK)
            
            a_count = output.lower().count('a')
            length_penalty = max(len(output) - self.config.max_length, 0)
            
            raw_fitness = (
                a_count * self.config.fitness_weights["a_score"] +
                length_penalty * self.config.fitness_weights["length_penalty"]
            )
            max_fitness = max(max_fitness, raw_fitness)
            min_fitness = min(min_fitness, raw_fitness)
            agent.fitness = raw_fitness  # Temporary storage

        # Second pass: normalize to 0.0-1.0 range
        for agent in population:
            if max_fitness != min_fitness:
                agent.fitness = (agent.fitness - min_fitness) / (max_fitness - min_fitness)
            else:
                agent.fitness = 0.5  # All agents equal
            
    def generate_initial(self) -> Chromosome:
        """Generate random initial string with some 'a's as a TASK chromosome"""
        length = random.randint(15, 30)
        vowels = ['a' if random.random() < 0.3 else chr(random.randint(97,122)) 
                for _ in range(length)]
        return Chromosome(ChromosomeType.TASK, ''.join(vowels))

    def mutate(self, chromosome: Chromosome, mutation_rate: float) -> Chromosome:
        """Mutate a string chromosome with character flips and length changes"""
        if chromosome.type != ChromosomeType.TASK:
            return chromosome  # Only mutate task chromosomes
        
        chars = list(chromosome.value)
        
        # Character mutations using enumerate
        for i, char in enumerate(chars):
            if random.random() < mutation_rate:
                chars[i] = random.choice('abcdefghijklmnopqrstuvwxyz')  # pylint: disable=consider-using-enumerate
        
        # Length mutation (10% chance to add/remove)
        if random.random() < 0.1:
            if random.random() < 0.5 and len(chars) > 1:
                chars.pop(random.randint(0, len(chars)-1))
            else:
                chars.append(random.choice('abcdefghijklmnopqrstuvwxyz'))
        
        return Chromosome(chromosome.type, ''.join(chars))
