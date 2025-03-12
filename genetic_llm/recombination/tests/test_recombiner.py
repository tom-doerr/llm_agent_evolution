import pytest
from genetic_llm.recombination import DSPyRecombiner

class TestDSPyRecombiner:
    def test_combine_returns_string(self):
        recombiner = DSPyRecombiner()
        result = recombiner.combine("parent1", "parent2")
        assert isinstance(result, str)
