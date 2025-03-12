from abc import ABC, abstractmethod

class RecombinerABC(ABC):
    @abstractmethod
    def combine(self, parent1: str, parent2: str) -> str:
        """Combine two chromosome strings into new offspring"""
