from unittest.mock import Mock
from genetic_llm.core import GeneticConfig, ChromosomeType
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.evolution import EvolutionEngine
from .test_evolution import TestConcreteEvolutionEngine, TestAgent

class TestEvolutionEdgeCases:
    def test_single_parent_population(self):
        config = GeneticConfig(population_size=5, elite_size=1)
        engine = TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
            config, DSPyMateSelector(), DSPyRecombiner(), Mock()  # pylint: disable=abstract-class-instantiated
        )
        
        population = [TestAgent({ct: "clone" for ct in ChromosomeType}, fitness=10)] * 5
        new_pop = engine.evolve_population(population)
        
        assert len(new_pop) == 5
        assert all(agent.chromosomes == population[0].chromosomes for agent in new_pop)

    def test_minimum_population_size(self):
        config = GeneticConfig(population_size=2, elite_size=1)
        engine = TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
            config, DSPyMateSelector(), DSPyRecombiner(), Mock()  # pylint: disable=abstract-class-instantiated
        )
        
        population = [
            TestAgent({ct: "A" for ct in ChromosomeType}, fitness=10),
            TestAgent({ct: "B" for ct in ChromosomeType}, fitness=5)
        ]
        new_pop = engine.evolve_population(population)
        
        assert new_pop[0].fitness == 10  # Elite preserved
        assert any(agent.chromosomes[ChromosomeType.DNA] == "A" for agent in new_pop)  # pylint: disable=no-member
