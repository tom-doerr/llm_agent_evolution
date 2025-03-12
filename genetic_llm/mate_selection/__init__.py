import dspy
from typing import List
from genetic_llm.core import Agent
from genetic_llm.mate_selection_abc import MateSelector

class DSPyMateSelector(MateSelector, dspy.Module):
    def __init__(self):
        super().__init__()
        self.lm = dspy.LM('openrouter/google/gemini-2.0-flash-001')
        self.select_mate = dspy.Predict("agent_chromosomes, population_fitness -> selected_mate")

    def select(self, population: List[Agent]) -> Agent:
        prediction = self.select_mate(
            agent_chromosomes=population[0].chromosomes,
            population_fitness=[a.fitness for a in population]
        )
        return prediction.selected_mate
