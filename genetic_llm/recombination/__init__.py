import dspy
from genetic_llm.recombination_abc import RecombinerABC

class Meta(type):
    """Combined metaclass for RecombinerABC and dspy.Module"""
    def __new__(cls, name, bases, namespace, **kwargs):
        return type.__new__(type, name, bases, namespace)
        
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return super().__prepare__(name, bases, **kwargs)

class DSPyRecombiner(RecombinerABC, dspy.Module, metaclass=type("Meta", (type(RecombinerABC), type(dspy.Module)), {})):
    def __init__(self) -> None:
        super().__init__()
        self.lm = dspy.LM('openrouter/google/gemini-2.0-flash-001')
        self.recombine = dspy.ChainOfThought("parent1_chromosome, parent2_chromosome -> child_chromosome, rationale::string")

    def combine(self, parent1: str, parent2: str) -> str:
        if not isinstance(parent1, str) or not isinstance(parent2, str):
            raise ValueError("Both parents must be strings")
        if not parent1 and not parent2:
            return ""
            
        result = self.recombine(
            parent1_chromosome=parent1,
            parent2_chromosome=parent2
        )
        
        if not hasattr(result, 'child_chromosome'):
            raise RuntimeError("Recombination failed - missing child_chromosome in response")
            
        return str(result.child_chromosome)
# Package initialization
