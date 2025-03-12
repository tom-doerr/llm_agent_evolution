import inspect

from genetic_llm.mate_selection_abc import MateSelector
from genetic_llm.recombination_abc import RecombinerABC

def test_mate_selector_abc():
    # Verify MateSelector ABC module defines __all__ with exactly "MateSelector"
    import genetic_llm.mate_selection_abc as msa
    assert hasattr(msa, "__all__"), "Module mate_selection_abc must define __all__"
    assert isinstance(msa.__all__, list), "__all__ must be a list"
    assert "MateSelector" in msa.__all__, "MateSelector must be in __all__"
    # Ensure MateSelector is abstract
    assert inspect.isabstract(MateSelector), "MateSelector should be an abstract class"

def test_recombiner_abc():
    # Verify RecombinerABC module defines __all__ with exactly "RecombinerABC"
    import genetic_llm.recombination_abc as ra
    assert hasattr(ra, "__all__"), "Module recombination_abc must define __all__"
    assert isinstance(ra.__all__, list), "__all__ must be a list"
    assert "RecombinerABC" in ra.__all__, "RecombinerABC must be in __all__"
    # Ensure RecombinerABC is abstract
    assert inspect.isabstract(RecombinerABC), "RecombinerABC should be an abstract class"
