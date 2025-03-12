import dspy
from genetic_llm.recombination_abc import RecombinerABC

class DSPyRecombiner(RecombinerABC, dspy.Module):
    __metaclass__ = type(dspy.Module)  # Resolve metaclass conflict
    
    def __init__(self) -> None:
        super().__init__()
        self.lm = dspy.LM('openrouter/google/gemini-2.0-flash-001')
        self.recombine = dspy.Predict("parent1_chromosome, parent2_chromosome -> child_chromosome")

    def combine(self, parent1: str, parent2: str) -> str:
        if not isinstance(parent1, str) or not isinstance(parent2, str):
            raise ValueError("Both parents must be strings")
        if not parent1 and not parent2:
            return ""
            
        with dspy.context(lm=self.lm):
            result = self.recombine(
                parent1_chromosome=parent1,
                parent2_chromosome=parent2
            )
        
        return getattr(result, 'child_chromosome', '')
# Package initialization
