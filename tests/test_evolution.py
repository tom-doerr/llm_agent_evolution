from genetic_llm.evolution import EvolutionEngine
from genetic_llm.core import Agent, GeneticConfig, ChromosomeType
from genetic_llm.mate_selection_abc import MateSelector
from genetic_llm.recombination_abc import RecombinerABC

# Dummy implementations that bypass external dependencies
class DummyMateSelector(MateSelector):
    def select(self, population: list) -> Agent:
        # Always select the first agent as mate
        return population[0]

class DummyRecombiner(RecombinerABC):
    def combine(self, parent1: str, parent2: str) -> str:
        # Simple combination: concatenate the two parent strings with an underscore
        return parent1 + "_" + parent2

def test_evolve_population():
    # Configure a small population and a couple of elites in a single call
    engine = EvolutionEngine(GeneticConfig(population_size=10, elite_size=2),
                             DummyMateSelector(),
                             DummyRecombiner())

    # Create an initial population with decreasing fitness values
    population = []
    for i in range(engine.config.population_size):
        chromosomes = {
            ChromosomeType.TASK: f"task_{i}",
            ChromosomeType.MATE_SELECTION: f"mate_{i}",
            ChromosomeType.RECOMBINATION: f"recomb_{i}"
        }
        agent = Agent(chromosomes)
        agent.fitness = engine.config.population_size - i  # Higher fitness for lower i values
        population.append(agent)

    new_population = engine.evolve_population(population)

    # Verify that the evolved population has the correct size
    assert len(new_population) == engine.config.population_size

    # Verify that elite agents (the highest fitness ones) are preserved in the new population
    sorted_population = sorted(population, key=lambda a: a.fitness, reverse=True)
    elites = sorted_population[:engine.config.elite_size]
    for elite in elites:
        assert elite in new_population
