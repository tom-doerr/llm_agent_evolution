import dspy
from genetic_llm.core import Agent
from .mate_selection_abc import MateSelector

class DSPyMateSelector(MateSelector, dspy.Module):
    def __init__(self, model: str = 'openrouter/google/gemini-2.0-flash-001'):
        super().__init__()
        self.lm = dspy.LM(model)
        self.select_mate = dspy.Predict(
            "population_chromosomes, population_fitness -> selected_index",
            instructions="Select a 0-based index of the most promising agent from the population. Return ONLY the integer index."
        )

    def select(self, population: list[Agent]) -> Agent:
        if not population:
            raise ValueError("Cannot select from empty population")
            
        population_chromosomes = []
        population_fitness = []
        for agent in population:
            population_chromosomes.append(agent.chromosomes)
            population_fitness.append(agent.fitness)
        
        with dspy.context(lm=self.lm):
            prediction = self.select_mate(
                population_chromosomes=population_chromosomes,
                population_fitness=population_fitness
            )
        
        try:
            index = int(float(prediction.selected_index.strip()))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid index returned by model: {prediction.selected_index}") from e
            
        if not 0 <= index < len(population):
            raise IndexError(f"Selected index {index} out of bounds [0-{len(population)-1}]")
            
        return population[index]
# Package initialization
