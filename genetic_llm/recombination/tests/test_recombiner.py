import pytest
from unittest.mock import Mock, call, patch
import dspy
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.recombination_abc import RecombinerABC

@pytest.fixture(name="mock_recombine_fixture")
def mock_recombine_fixture(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(dspy, 'ChainOfThought', lambda _: mock)
    return mock

class TestDSPyRecombiner:  # pylint: disable=too-many-public-methods
    def test_implements_interface(self):
        assert issubclass(DSPyRecombiner, RecombinerABC)
        assert issubclass(DSPyRecombiner, dspy.Module)

    def test_combine_valid_parents(self, mock_recombine):
        mock_recombine.return_value = Mock(child_chromosome=12345)
        recombiner = DSPyRecombiner()
        result = recombiner.combine("ABCDEF", "GHIJKL")
        assert result == "12345"

    def test_combine_empty_parents(self):
        recombiner = DSPyRecombiner()
        result = recombiner.combine("", "")
        assert result == ""

    def test_combine_error_handling(self, mock_recombine):
        mock_recombine.side_effect = Exception("API error")
        recombiner = DSPyRecombiner()
        result = recombiner.combine("123", "abc")
        assert result == ""

    def test_invalid_input_types(self):
        recombiner = DSPyRecombiner()
        with pytest.raises(ValueError):
            recombiner.combine(123, "abc")

    @pytest.mark.parametrize("parent1, parent2", [
        ("", "valid"),
        ("valid", "")
    ])
    def test_combine_with_empty_parent(self, parent1, parent2):
        # Test doesn't need mock since empty parent handling is done before LM call
        recombiner = DSPyRecombiner()
        assert recombiner.combine(parent1, parent2) == ""  # Should return empty per interface

    @pytest.mark.parametrize("mock_response", [
        {"child_chromosome": None},
        Mock(spec=[])
    ])
    def test_combine_unexpected_lm_output(self, mock_recombine, mock_response):
        mock_recombine.return_value = mock_response
        recombiner = DSPyRecombiner()
        assert recombiner.combine("A", "B") == ""

    def test_retry_success_after_failures(self, mock_recombine):
        mock_recombine.side_effect = [
            Exception("Error 1"),
            Exception("Error 2"),
            Mock(child_chromosome="success")
        ]
        with patch('time.sleep') as mock_sleep:
            recombiner = DSPyRecombiner()
            result = recombiner.combine("A", "B")
            assert result == "success"
            assert mock_recombine.call_count == 3
            mock_sleep.assert_has_calls([call(1), call(2)])

    def test_retry_exhausted(self, mock_recombine):
        mock_recombine.side_effect = Exception("Persistent error")
        with patch('time.sleep') as mock_sleep:
            recombiner = DSPyRecombiner()
            result = recombiner.combine("A", "B")
            assert result == ""
            assert mock_recombine.call_count == 3
            assert mock_sleep.call_count == 2
