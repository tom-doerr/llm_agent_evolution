import inspect
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.mate_selection_abc import MateSelector
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.recombination_abc import RecombinerABC

def test_dspy_mate_selector_concrete():
    # Verify DSPyMateSelector correctly implements the MateSelector interface
    assert issubclass(DSPyMateSelector, MateSelector), "DSPyMateSelector should be a subclass of MateSelector"
    assert not inspect.isabstract(DSPyMateSelector), "DSPyMateSelector should implement all abstract methods"

def test_dspy_recombiner_concrete():
    # Verify DSPyRecombiner correctly implements the RecombinerABC interface
    assert issubclass(DSPyRecombiner, RecombinerABC), "DSPyRecombiner should be a subclass of RecombinerABC"
    assert not inspect.isabstract(DSPyRecombiner), "DSPyRecombiner should implement all abstract methods"
