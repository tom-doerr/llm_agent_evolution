from abc import ABC, ABCMeta, abstractmethod

class RecombinerABC(ABC, metaclass=ABCMeta):
    @abstractmethod
    def combine(self, parent1: str, parent2: str) -> str:
        """Combine two chromosome strings into new offspring"""
