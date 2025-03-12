import logging
import time
import dspy
from genetic_llm.recombination_abc import RecombinerABC

logger = logging.getLogger(__name__)

class DSPyRecombiner(RecombinerABC, dspy.Module, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()
        self.lm = dspy.LM('openrouter/google/gemini-2.0-flash-001')
        self.recombine = dspy.ChainOfThought("parent1_chromosome, parent2_chromosome -> child_chromosome")

    def combine(self, parent1: str, parent2: str) -> str:
        if not isinstance(parent1, str) or not isinstance(parent2, str):
            raise ValueError("Both parents must be strings")
        if not parent1 and not parent2:
            return ""
        
        max_retries = 3
        base_delay = 1  # seconds
        for attempt in range(max_retries):
            try:
                with dspy.context(lm=self.lm):
                    result = self.recombine(
                        parent1_chromosome=parent1,
                        parent2_chromosome=parent2
                    )
                child = str(getattr(result, 'child_chromosome', '')) or ''
                return child
            except RuntimeError as e:  # More specific exception type
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning("Recombination attempt %d/%d failed. Retrying in %.1fs. Error: %s",
                                   attempt + 1, max_retries, delay, e)
                    time.sleep(delay)
                else:
                    logger.error("Recombination failed after %d attempts. Parents: '%s', '%s'. Error: %s",
                                 max_retries, parent1, parent2, e)
                    return ""
        return ""  # Should never be reached
# Package initialization
