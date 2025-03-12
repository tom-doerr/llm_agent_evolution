from genetic_llm.core_abc import PopulationEvaluatorABC
from genetic_llm.core import Agent, GeneticConfig, Chromosome, ChromosomeType
import random

class StringOptimizationEvaluator(PopulationEvaluatorABC):
    """Evaluates strings based on 'a' count and length constraints"""
    def __init__(self, config: GeneticConfig):
        self.config = config
        
    def evaluate(self, population: list[Agent]) -> None:  # pylint: disable=too-many-locals
        for agent in population:
            # Get the output string from the task chromosome
            output = next(c.value for c in agent.chromosomes 
                        if c.type.name == "TASK")
            
            # Calculate fitness components
            a_count = output.lower().count('a')
            length_penalty = max(len(output) - self.config.max_length, 0)
            
            # Apply weighted fitness formula
            agent.fitness = (
                a_count * self.config.fitness_weights["a_score"] +
                length_penalty * self.config.fitness_weights["length_penalty"]
            )
            
    def generate_initial(self) -> Chromosome:
        """Generate random initial string with some 'a's as a TASK chromosome"""
        length = random.randint(15, 30)
        vowels = ['a' if random.random() < 0.3 else chr(random.randint(97,122)) 
                for _ in range(length)]
        return Chromosome(ChromosomeType.TASK, ''.join(vowels))
