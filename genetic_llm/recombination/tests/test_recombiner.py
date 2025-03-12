import pytest
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.recombination_abc import RecombinerABC

class TestDSPyRecombiner:
    def test_implements_abc(self):
        assert issubclass(DSPyRecombiner, RecombinerABC)
    def test_combine_valid_parents(self) -> None:
        recombiner = DSPyRecombiner()
        parent_a = "ABCDEF"
        parent_b = "GHIJKL"
        child = recombiner.combine(parent_a, parent_b)
        
        assert isinstance(child, str)
        assert len(child) > 0
        assert any(c in child for c in parent_a)
        assert any(c in child for c in parent_b)

    def test_combine_empty_parents(self) -> None:
        recombiner = DSPyRecombiner()
        assert recombiner.combine("", "") == ""

    def test_combine_mixed_parents(self) -> None:
        recombiner = DSPyRecombiner()
        child = recombiner.combine("123", "abc")
        assert any(c.isdigit() for c in child)
        assert any(c.isalpha() for c in child)

    def test_invalid_input_types(self) -> None:
        recombiner = DSPyRecombiner()
        with pytest.raises(ValueError) as excinfo:
            recombiner.combine(123, "abc")
        assert "Both parents must be strings" in str(excinfo.value)
        
        with pytest.raises(ValueError) as excinfo:
            recombiner.combine("abc", None)
        assert "Both parents must be strings" in str(excinfo.value)

    def test_single_empty_parent(self) -> None:
        recombiner = DSPyRecombiner()
        child = recombiner.combine("ABCDEF", "")
        assert isinstance(child, str)
        assert len(child) > 0
        assert any(c in child for c in "ABCDEF")
