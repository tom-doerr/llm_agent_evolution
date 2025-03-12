from abc import ABC, abstractmethod
from typing import List, Dict
from genetic_llm.core import AgentABC, ChromosomeType

class EvolutionEngineABC(ABC):
    """Abstract base class defining the interface for evolution engines"""
    
    @abstractmethod
    def __init__(self, config: 'GeneticConfig'):
        """Initialize evolution engine with configuration
        Args:
            config: Genetic configuration parameters
        """
        
    @abstractmethod
    def evolve_population(self, population: List[AgentABC]) -> List[AgentABC]:
        """Generate new population from existing one through selection and recombination
        Args:
            population: Current generation of agents
        Returns:
            New population of agents
        """
        
    @abstractmethod
    def _validate_chromosomes(self, chromosomes: Dict[ChromosomeType, str]) -> None:
        """Validate chromosome structure meets implementation requirements
        Args:
            chromosomes: Dictionary of chromosome types to their string values
        Raises:
            ValueError: If any chromosome fails validation
        """
