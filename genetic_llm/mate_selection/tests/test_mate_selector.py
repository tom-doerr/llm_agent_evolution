import pytest
import dspy
from unittest import mock
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.core import Agent, ChromosomeType

class TestDSPyMateSelector:
    def test_select_returns_agent(self):
        selector = DSPyMateSelector()
        agents = [
            Agent({ChromosomeType.MATE_SELECTION: "agent1"}),
            Agent({ChromosomeType.MATE_SELECTION: "agent2"}),
            Agent({ChromosomeType.MATE_SELECTION: "agent3"}),
        ]
        selected = selector.select(agents)
        assert selected in agents

    def test_empty_population_raises_error(self):
        selector = DSPyMateSelector()
        with pytest.raises(ValueError):
            selector.select([])

    def test_invalid_index_raises_error(self):
        selector = DSPyMateSelector()
        agents = [Agent({ChromosomeType.MATE_SELECTION: "test"})]
        
        # Patch the prediction to return invalid index
        with mock.patch.object(selector.select_mate, 'predict', return_value=dspy.Prediction(selected_index="invalid")):
            with pytest.raises(ValueError):
                selector.select(agents)
