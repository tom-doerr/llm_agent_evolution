import dspy
from genetic_llm.core import RecombinerABC

class DSPyRecombiner(RecombinerABC, dspy.Module):
    def __init__(self):
        super().__init__()
        self.lm = dspy.LM('openrouter/google/gemini-2.0-flash-001')
        self.recombine = dspy.Predict("parent1_chromosome, parent2_chromosome -> child_chromosome")

    def combine(self, parent1: str, parent2: str) -> str:
        result = self.recombine(
            parent1_chromosome=parent1,
            parent2_chromosome=parent2
        )
        return result.child_chromosome
