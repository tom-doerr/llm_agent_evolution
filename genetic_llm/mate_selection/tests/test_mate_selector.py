import pytest
import dspy
from unittest import mock
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.core import Agent
from genetic_llm.mate_selection_abc import MateSelector  # ChromosomeType removed

class TestDSPyMateSelector:
    def test_implements_abc(self):
        assert issubclass(DSPyMateSelector, MateSelector)
    def test_select_returns_valid_agent(self):
        selector = DSPyMateSelector()
        agents = [
            Agent({"strategy": "A", "parameters": "X"}),
            Agent({"strategy": "B", "parameters": "Y"}),
            Agent({"strategy": "C", "parameters": "Z"})
        ]
        
        # Mock a valid prediction
        with mock.patch.object(selector.select_mate, 'predict', 
                            return_value=dspy.Prediction(selected_index="1")):
            selected = selector.select(agents)
            assert selected == agents[1]

    def test_empty_population_raises_error(self):
        selector = DSPyMateSelector()
        with pytest.raises(ValueError):
            selector.select([])

    @pytest.mark.parametrize("index, expected_error", [
        ("invalid", ValueError),
        ("-1", IndexError),
        ("3", IndexError),
        ("NaN", ValueError)
    ])
    def test_invalid_indices_raise_errors(self, index, expected_error):
        selector = DSPyMateSelector()
        agents = [Agent({"strategy": "A"}), Agent({"strategy": "B"}), Agent({"strategy": "C"})]
        
        with mock.patch.object(selector.select_mate, 'predict',
                             return_value=dspy.Prediction(selected_index=index)):
            with pytest.raises(expected_error):
                selector.select(agents)
