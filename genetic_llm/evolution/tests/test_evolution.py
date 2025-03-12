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
        config = GeneticConfig(population_size=10)
        engine = EvolutionEngine(
            config,
            DSPyMateSelector(),
            DSPyRecombiner()
        )
        population = [Agent({ct: "test" for ct in ChromosomeType}) for _ in range(10)]
        new_pop = engine.evolve_population(population)
        assert len(new_pop) == config.population_size
