import pytest
import dspy
from unittest import mock
from genetic_llm.mate_selection import DSPyMateSelector, MateSelector
from genetic_llm.core import Agent

# Concrete test implementation with required abstract methods
class TestAgent(Agent):
    def __init__(self, chromosomes):
        super().__init__(chromosomes)
        self._fitness = 0.0  # Add concrete fitness attribute
    
    @property
    def fitness(self):
        return self._fitness
    
    @fitness.setter
    def fitness(self, value):
        self._fitness = value

class TestDSPyMateSelector:
    def test_implements_abc(self):
        assert issubclass(DSPyMateSelector, MateSelector)
    def test_select_returns_valid_agent(self):
        selector = DSPyMateSelector()
        agents = [
            TestAgent({"strategy": "A", "parameters": "X"}),
            TestAgent({"strategy": "B", "parameters": "Y"}),
            TestAgent({"strategy": "C", "parameters": "Z"})
        ]
        
        # Mock __call__ instead of predict
        with mock.patch.object(selector.select_mate, '__call__', 
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
        agents = [TestAgent({"strategy": "A"}), TestAgent({"strategy": "B"}), TestAgent({"strategy": "C"})]
        
        with mock.patch.object(selector.select_mate, '__call__',
                             return_value=dspy.Prediction(selected_index=index)):
            with pytest.raises(expected_error):
                selector.select(agents)
