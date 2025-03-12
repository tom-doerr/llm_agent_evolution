import pytest
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.core import Agent, ChromosomeType

class TestDSPyMateSelector:
    def test_select_returns_agent(self):
        selector = DSPyMateSelector()
        population = [
            Agent({
                ChromosomeType.MATE_SELECTION: "test",
                ChromosomeType.TASK: "test",
                ChromosomeType.RECOMBINATION: "test"
            })
        ]
        selected = selector.select(population)
        assert isinstance(selected, Agent)
