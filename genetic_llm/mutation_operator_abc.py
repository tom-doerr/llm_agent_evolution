from abc import ABC, abstractmethod

class MutationOperatorABC(ABC):
    @abstractmethod
    def mutate(self, chromosome: str, mutation_rate: float) -> str:
        """Mutate a chromosome with given mutation probability"""
