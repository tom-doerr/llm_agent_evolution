from typing import NamedTuple
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.core import Agent, ChromosomeType

# Dummy prediction object to simulate dspy.Predict output
class DummyPrediction(NamedTuple):
    selected_mate: Agent

# Create a subclass that overrides select to avoid dspy dependencies
class DummyDSPyMateSelector(DSPyMateSelector):
    def __init__(self):
        # Do not initialize the dspy components
        pass
    def select(self, population: list) -> Agent:
        return DummyPrediction(selected_mate=population[0])

def test_select_returns_correct_agent():
    # Create a dummy population with one agent for simplicity
    agent = Agent({
        ChromosomeType.TASK: "task",
        ChromosomeType.MATE_SELECTION: "mate_selection",
        ChromosomeType.RECOMBINATION: "recombination"
    })
    agent.fitness = 10.0
    population = [agent]
    selector = DummyDSPyMateSelector()
    selected = selector.select(population)
    assert selected == agent
