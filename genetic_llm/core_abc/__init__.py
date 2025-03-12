from abc import ABC, abstractmethod
from typing import Dict, Type
from . import ChromosomeType

class GeneticConfigABC(ABC):
    @abstractmethod
    @classmethod
    def validate_size(cls, population_size: int) -> bool:
        """Validate population size meets implementation constraints"""
        
    @abstractmethod
    @classmethod
    def validate_mutation_rate(cls, rate: float) -> bool:
        """Validate mutation rate is within acceptable bounds"""

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
from enum import Enum

class ChromosomeType(Enum):
    BEHAVIOR = "behavior"
    KNOWLEDGE = "knowledge" 
    STRATEGY = "strategy"
