import pytest
from unittest.mock import Mock
import dspy
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.recombination_abc import RecombinerABC

class TestDSPyRecombiner:
    def test_implements_interface(self):
        # Test both parent classes
        assert issubclass(DSPyRecombiner, RecombinerABC)
        assert issubclass(DSPyRecombiner, dspy.Module)

    @pytest.fixture
    def mock_recombine(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr(dspy, 'ChainOfThought', lambda _: mock)
        return mock

    @pytest.mark.parametrize("parent1, parent2, expected, test_id", [
        ("ABCDEF", "GHIJKL", "12345", "valid_parents"),
        ("", "", "", "empty_parents"),
        ("123", "abc", "", "error_handling")
    ])
    def test_combine_scenarios(self, mock_recombine, parent1, parent2, expected, test_id):
        recombiner = DSPyRecombiner()
        if test_id == "valid_parents":
            mock_recombine.return_value = Mock(child_chromosome=12345)
        elif test_id == "error_handling":
            mock_recombine.side_effect = Exception("API error")
            
        result = recombiner.combine(parent1, parent2)
        assert result == expected

    def test_invalid_input_types(self):
        recombiner = DSPyRecombiner()
        with pytest.raises(ValueError):
            recombiner.combine(123, "abc")

    @pytest.mark.parametrize("parents", [
        ("", "valid"),
        ("valid", "")
    ])
    def test_combine_with_empty_parent(self, mock_recombine, parents):
        parent1, parent2 = parents
        mock_recombine.return_value = Mock(child_chromosome="hybrid")
        recombiner = DSPyRecombiner()
        assert recombiner.combine(parent1, parent2) == "hybrid"

    @pytest.mark.parametrize("mock_response", [
        {"child_chromosome": None},
        Mock(spec=[])
    ])
    def test_combine_unexpected_lm_output(self, mock_recombine, mock_response):
        mock_recombine.return_value = mock_response
        recombiner = DSPyRecombiner()
        assert recombiner.combine("A", "B") == ""
