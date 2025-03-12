import pytest
from unittest.mock import Mock
from genetic_llm.evolution import EvolutionEngine
from genetic_llm.core import GeneticConfig, ChromosomeType
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.evolution_abc import EvolutionEngineABC

# Test concrete implementation
class TestConcreteEvolutionEngine(EvolutionEngine):
    """Concrete implementation for testing abstract base class functionality""" 

# Test double for abstract Agent class
class TestAgent:
    def __init__(self, chromosomes, fitness=0):
        self.chromosomes = chromosomes
        self.fitness = fitness

class TestEvolutionEngineBasics:
    def test_implements_abc(self):
        assert issubclass(EvolutionEngine, EvolutionEngineABC)
    def test_evolve_population_size_remains_constant(self):
        config = GeneticConfig(population_size=10, elite_size=2)
        engine = TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
            config, DSPyMateSelector(), DSPyRecombiner(), Mock()  # pylint: disable=abstract-class-instantiated
        )
        population = [TestAgent({ct: "test" for ct in ChromosomeType}) for _ in range(10)]
        new_pop = engine.evolve_population(population)
        assert len(new_pop) == config.population_size
    
    def test_elites_are_preserved(self):
        config = GeneticConfig(population_size=10, elite_size=2)
        engine = TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
            config, DSPyMateSelector(), DSPyRecombiner(), Mock()
        )
        
        # Create population with ascending fitness
        population = [TestAgent({ct: str(i) for ct in ChromosomeType}, fitness=i) for i in range(10)]
        new_pop = engine.evolve_population(population)
        
        # Top 2 should be highest fitness agents
        assert new_pop[0].fitness == 9
        assert new_pop[1].fitness == 8
    
    def test_invalid_elite_size_raises_error(self):
        config = GeneticConfig(population_size=5, elite_size=10)
        with pytest.raises(ValueError, match="Elite size cannot exceed population size"):
            TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
                config, DSPyMateSelector(), DSPyRecombiner(), Mock()
            )

    def test_tied_fitness_elite_selection(self):
        config = GeneticConfig(population_size=5, elite_size=2)
        engine = TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
            config, DSPyMateSelector(), DSPyRecombiner(), Mock()
        )
        
        population = [
            TestAgent({"dna": "A"}, fitness=10),
            TestAgent({"dna": "B"}, fitness=10),  # Tie for first
            TestAgent({"dna": "C"}, fitness=5),
            TestAgent({"dna": "D"}, fitness=5),
            TestAgent({"dna": "E"}, fitness=1)
        ]
        new_pop = engine.evolve_population(population)
        
        # Should preserve both top 10 fitness agents
        assert sum(1 for a in new_pop if a.fitness == 10) == 2

