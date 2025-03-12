from abc import ABC, abstractmethod
from typing import List
from ..core import Agent

class MateSelector(ABC):
    @abstractmethod
    def select(self, population: List[Agent]) -> Agent:
        """Select a mate from population based on strategy"""
__all__ = ["MateSelector"]
