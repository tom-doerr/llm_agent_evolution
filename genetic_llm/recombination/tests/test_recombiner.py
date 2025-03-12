import pytest
from unittest.mock import Mock
import dspy
from genetic_llm.recombination import DSPyRecombiner

class TestDSPyRecombiner:
    def test_implements_interface(self):
        assert isinstance(DSPyRecombiner(), dspy.Module)

    @pytest.fixture
    def mock_recombine(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr(dspy, 'ChainOfThought', lambda _: mock)
        return mock

    def test_combine_valid_parents(self, mock_recombine):
        mock_recombine.return_value = Mock(child_chromosome="ABCDEFGHIJKL")
        recombiner = DSPyRecombiner()
        result = recombiner.combine("ABCDEF", "GHIJKL")
        assert result == "ABCDEFGHIJKL"

    def test_combine_empty_parents(self):
        recombiner = DSPyRecombiner()
        assert recombiner.combine("", "") == ""

    def test_combine_error_handling(self, mock_recombine):
        mock_recombine.side_effect = Exception("API error")
        recombiner = DSPyRecombiner()
        result = recombiner.combine("123", "abc")
        assert result == ""  # Default empty response on error
