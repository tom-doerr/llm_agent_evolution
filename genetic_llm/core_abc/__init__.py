from abc import ABC, abstractmethod
from typing import Dict
from . import ChromosomeType

class AgentABC(ABC):
    @abstractmethod
    def __init__(self, chromosomes: Dict[ChromosomeType, str]):
        """Initialize agent with chromosomes dictionary"""
        
    @property
    @abstractmethod
    def fitness(self) -> float:
        """Get agent's fitness score"""
        
    @fitness.setter
    @abstractmethod
    def fitness(self, value: float):
        """Set agent's fitness score"""

class PopulationEvaluatorABC(ABC):
    @abstractmethod
    def evaluate(self, population: list[AgentABC]) -> None:
        """Evaluate and assign fitness to population"""
