import logging
import dspy
from genetic_llm.core import Agent
from .mate_selection_abc import MateSelector

logging.basicConfig(level=logging.INFO)

    def _get_population_data(self, population: list[Agent]) -> dict:
        """Validate and extract population data for model input."""
        chromosomes = []
        fitness = []
        for agent in population:
            if not hasattr(agent, 'fitness') or agent.fitness is None:
                raise ValueError(f"Agent {agent} missing required fitness value")
            chromosomes.append(agent.chromosomes)
            fitness.append(agent.fitness)
        
        return {
            "population_chromosomes": chromosomes,
            "population_fitness": fitness
        }

class DSPyMateSelector(MateSelector, dspy.Module):
    def __init__(self, model: str = 'openrouter/google/gemini-2.0-flash-001'):
        super().__init__()
        self.lm = dspy.LM(model)
        self.select_mate = dspy.Predict(
            "population_chromosomes, population_fitness -> selected_index",
            instructions=(
                "Select the 0-based integer index of the most promising agent. "
                "Your response MUST be a single integer between 0 and {population_size-1}. "
                "Non-integer responses will cause system errors."
            )
        )

    def select(self, population: list[Agent]) -> Agent:
        if not population:
            raise ValueError("Cannot select from empty population")

        # Extract population data with validation
        pop_data = self._get_population_data(population)
        
        with dspy.context(lm=self.lm):
            prediction = self.select_mate(**pop_data)
        
        # Log raw model response
        logging.debug("Model selection response: %s", prediction.selected_index)
        
        try:
            index = int(float(prediction.selected_index.strip()))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid index returned by model: {prediction.selected_index}") from e
            
        if not 0 <= index < len(population):
            raise IndexError(f"Selected index {index} out of bounds [0-{len(population)-1}]")
            
        return population[index]
# Package initialization
