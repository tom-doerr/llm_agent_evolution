import pytest
from unittest.mock import Mock
from genetic_llm.evolution import EvolutionEngine
from genetic_llm.core import GeneticConfig, ChromosomeType
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.evolution_abc import EvolutionEngineABC

# Test double for abstract Agent class
class TestAgent:
    def __init__(self, chromosomes, fitness=0):
        self.chromosomes = chromosomes
        self.fitness = fitness

class TestEvolutionEngine:
    def test_implements_abc(self):
        assert issubclass(EvolutionEngine, EvolutionEngineABC)
    def test_evolve_population_size_remains_constant(self):
        config = GeneticConfig(population_size=10, elite_size=2)
        engine = EvolutionEngine(config, DSPyMateSelector(), DSPyRecombiner(), Mock())
        population = [TestAgent({ct: "test" for ct in ChromosomeType}) for _ in range(10)]
        new_pop = engine.evolve_population(population)
        assert len(new_pop) == config.population_size
    
    def test_elites_are_preserved(self):
        config = GeneticConfig(population_size=10, elite_size=2)
        mock_evaluator = Mock()
        engine = EvolutionEngine(config, DSPyMateSelector(), DSPyRecombiner(), mock_evaluator)
        
        population = [TestAgent({ct: str(i) for ct in ChromosomeType}, fitness=i) for i in range(10)]
        new_pop = engine.evolve_population(population)
        
        assert {agent.fitness for agent in new_pop[:2]} == {9, 8}
    
    def test_invalid_elite_size_raises_error(self):
        config = GeneticConfig(population_size=5, elite_size=10)
        with pytest.raises(ValueError, match="Elite size cannot exceed population size"):
            EvolutionEngine(config, DSPyMateSelector(), DSPyRecombiner(), Mock())

    def test_tied_fitness_elite_selection(self):
        config = GeneticConfig(population_size=5, elite_size=2)
        engine = EvolutionEngine(config, DSPyMateSelector(), DSPyRecombiner(), Mock())
        
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

    def test_chromosome_types_preserved(self):
        config = GeneticConfig(population_size=10, elite_size=2)
        engine = EvolutionEngine(config, DSPyMateSelector(), DSPyRecombiner(), Mock())
        
        population = [TestAgent({"dna": "test", "meta": "data"}) for _ in range(10)]
        new_pop = engine.evolve_population(population)
        
        for agent in new_pop:
            assert "dna" in agent.chromosomes
            assert "meta" in agent.chromosomes
