import pytest
from genetic_llm.evolution import EvolutionEngine
from genetic_llm.core import GeneticConfig, Agent, ChromosomeType
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.evolution_abc import EvolutionEngineABC

class TestEvolutionEngine:
    def test_implements_abc(self):
        assert issubclass(EvolutionEngine, EvolutionEngineABC)
    def test_evolve_population_size_remains_constant(self):
        config = GeneticConfig(population_size=10, elite_size=2)
        engine = EvolutionEngine(config, DSPyMateSelector(), DSPyRecombiner())
        population = [Agent({ct: "test" for ct in ChromosomeType}) for _ in range(10)]
        new_pop = engine.evolve_population(population)
        assert len(new_pop) == config.population_size
    
    def test_elites_are_preserved(self):
        config = GeneticConfig(population_size=10, elite_size=2)
        engine = EvolutionEngine(config, DSPyMateSelector(), DSPyRecombiner())
        
        # Create population with unique fitness values
        population = [Agent({ct: str(i) for ct in ChromosomeType}, fitness=i) for i in range(10)]
        new_pop = engine.evolve_population(population)
        
        # Top 2 elites should be preserved
        assert any(agent.fitness == 9 for agent in new_pop)
        assert any(agent.fitness == 8 for agent in new_pop)
    
    def test_invalid_elite_size_raises_error(self):
        config = GeneticConfig(population_size=5, elite_size=10)
        engine = EvolutionEngine(config, DSPyMateSelector(), DSPyRecombiner())
        population = [Agent({ct: "test" for ct in ChromosomeType}) for _ in range(5)]
        
        with pytest.raises(ValueError):
            engine.evolve_population(population)
