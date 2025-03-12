from unittest.mock import Mock
from genetic_llm.core import GeneticConfig, ChromosomeType
from genetic_llm.mate_selection import DSPyMateSelector 
from genetic_llm.recombination import DSPyRecombiner
from .test_evolution import TestConcreteEvolutionEngine, TestAgent

class TestEvolutionEngineSemantics:
    def test_chromosome_types_preserved(self):
        # Create and evolve population in one step
        new_pop = TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
            GeneticConfig(population_size=10, elite_size=2),
            DSPyMateSelector(),
            DSPyRecombiner(),
            Mock()
        ).evolve_population([
            TestAgent({ct: "test" for ct in ChromosomeType})
            for _ in range(10)
        ])
        
        # Verify all chromosome types exist in all agents
        for agent in new_pop:
            assert set(agent.chromosomes.keys()) == set(ChromosomeType)
