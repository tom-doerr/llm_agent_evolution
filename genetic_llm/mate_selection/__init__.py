import dspy
from genetic_llm.core import Agent
from .mate_selection_abc import MateSelector

class DSPyMateSelector(MateSelector, dspy.Module):
    def __init__(self, model: str = 'openrouter/google/gemini-2.0-flash-001'):
        super().__init__()
        self.lm = dspy.LM(model)
        self.select_mate = dspy.Predict("population_chromosomes, population_fitness -> selected_index")

    def select(self, population: list[Agent]) -> Agent:
        if not population:
            raise ValueError("Cannot select from empty population")
            
        population_chromosomes = [agent.chromosomes for agent in population]
        population_fitness = [agent.fitness for agent in population]
        
        with dspy.context(lm=self.lm):
            prediction = self.select_mate(
                population_chromosomes=population_chromosomes,
                population_fitness=population_fitness
            )
        
        try:
            index = int(prediction.selected_index)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid index returned by model: {prediction.selected_index}") from e
            
        if not 0 <= index < len(population):
            raise IndexError(f"Selected index {index} out of bounds [0-{len(population)-1}]")
            
        return population[index]
# Package initialization
