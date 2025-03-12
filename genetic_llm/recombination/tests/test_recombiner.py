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

    def test_combine_valid_parents(self, mock_recombine):
        mock_recombine.return_value = Mock(child_chromosome=12345)  # Test non-string value
        recombiner = DSPyRecombiner()
        result = recombiner.combine("ABCDEF", "GHIJKL")
        assert result == "12345"  # Verify string conversion

    def test_combine_empty_parents(self):
        recombiner = DSPyRecombiner()
        assert recombiner.combine("", "") == ""

    def test_combine_error_handling(self, mock_recombine):
        mock_recombine.side_effect = Exception("API error")
        recombiner = DSPyRecombiner()
        result = recombiner.combine("123", "abc")
        assert result == ""  # Default empty response on error

    def test_invalid_input_types(self):
        recombiner = DSPyRecombiner()
        with pytest.raises(ValueError):
            recombiner.combine(123, "abc")

    def test_combine_one_empty_parent(self, mock_recombine):
        mock_recombine.return_value = Mock(child_chromosome="hybrid")
        recombiner = DSPyRecombiner()
        assert recombiner.combine("", "valid") == "hybrid"
        assert recombiner.combine("valid", "") == "hybrid"

    def test_combine_unexpected_lm_output(self, mock_recombine):
        mock_recombine.return_value = Mock(child_chromosome=None)
        recombiner = DSPyRecombiner()
        assert recombiner.combine("A", "B") == ""
        
        mock_recombine.return_value = Mock(spec=[])
        assert recombiner.combine("A", "B") == ""
