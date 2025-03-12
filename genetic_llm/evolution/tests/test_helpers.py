from genetic_llm.evolution import EvolutionEngine
from genetic_llm.evolution_abc import EvolutionEngineABC

# Test concrete implementation
class TestConcreteEvolutionEngine(EvolutionEngine):
    """Concrete implementation for testing abstract base class functionality"""

# Test double for abstract Agent class
class TestAgent:
    def __init__(self, chromosomes, fitness=0):
        self.chromosomes = chromosomes
        self.fitness = fitness
