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
    def test_select_returns_valid_agent(self):
        assert issubclass(DSPyMateSelector, MateSelector), "Must implement MateSelector ABC"
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
        ("3", IndexError),  # Population size 3 (0-2)
        ("two", ValueError),
        ("NaN", ValueError)
    ])
    def test_invalid_indices_raise_errors(self, index, expected_error):
        selector = DSPyMateSelector()
        agents = [TestAgent({"strategy": "A"}), TestAgent({"strategy": "B"}), TestAgent({"strategy": "C"})]
        
        with mock.patch.object(selector.select_mate, '__call__',
                             return_value=dspy.Prediction(selected_index=index)):
            with pytest.raises(expected_error):
                selector.select(agents)

    @pytest.mark.parametrize("index", ["0", "1 ", "2.0", " 2 "])
    def test_valid_indices(self, index):
        selector = DSPyMateSelector()
        agents = [
            TestAgent({"strategy": "A"}),
            TestAgent({"strategy": "B"}),
            TestAgent({"strategy": "C"})
        ]
        
        with mock.patch.object(selector.select_mate, '__call__',
                             return_value=dspy.Prediction(selected_index=index)):
            selected = selector.select(agents)
            assert selected in agents

    def test_input_data_format(self):
        selector = DSPyMateSelector()
        agents = [
            TestAgent({"a": 1}),
            TestAgent({"b": 2})
        ]
        agents[0].fitness = 0.8
        agents[1].fitness = 1.2

        with mock.patch.object(selector.select_mate, '__call__') as mock_predict:
            mock_predict.return_value = dspy.Prediction(selected_index="0")
            selector.select(agents)
            
            # Verify input format
            called_with = mock_predict.call_args[1]
            assert called_with["population_chromosomes"] == [{"a": 1}, {"b": 2}]
            assert called_with["population_fitness"] == [0.8, 1.2]
