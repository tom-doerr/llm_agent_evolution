from abc import ABC, abstractmethod
from typing import List
from genetic_llm.core import AgentABC

class EvolutionEngineABC(ABC):
    @abstractmethod
    def __init__(self, config: 'GeneticConfig'):
        """Initialize evolution engine with configuration"""
        
    @abstractmethod
    def evolve_population(self, population: List[AgentABC]) -> List[AgentABC]:
        """Generate new population from existing one"""
