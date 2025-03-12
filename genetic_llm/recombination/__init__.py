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
        self._validate_parents(parent1, parent2)
        if not parent1 and not parent2:
            return ""
        return self._retry_recombination(parent1, parent2)

    def _validate_parents(self, parent1: str, parent2: str) -> None:
        if not isinstance(parent1, str) or not isinstance(parent2, str):
            raise ValueError("Both parents must be strings")

    def _retry_recombination(self, parent1: str, parent2: str) -> str:
        for attempt in range(3):
            try:
                return self._attempt_recombination(parent1, parent2)
            except RuntimeError as e:
                self._handle_retry_error(attempt, e, parent1, parent2)
        return ""

    def _attempt_recombination(self, parent1: str, parent2: str) -> str:
        with dspy.context(lm=self.lm):
            result = self.recombine(
                parent1_chromosome=parent1,
                parent2_chromosome=parent2
            )
        return self._parse_result(result)

    def _parse_result(self, result) -> str:
        child = str(getattr(result, 'child_chromosome', ''))
        return child.strip() if child else ""

    def _handle_retry_error(self, attempt: int, error: Exception, parent1: str, parent2: str) -> None:
        if attempt >= 2:  # Final attempt
            logger.error("Recombination failed after 3 attempts. Parents: '%s', '%s'. Error: %s",
                         parent1, parent2, error)
            raise
        delay = 2 ** attempt
        logger.warning("Attempt %d/3 failed. Retrying in %ds. Error: %s",
                       attempt + 1, delay, error)
        time.sleep(delay)
# Package initialization
