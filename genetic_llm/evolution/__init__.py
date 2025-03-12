from genetic_llm.core import Agent, GeneticConfig
from genetic_llm.core_abc import AgentABC
from genetic_llm.mate_selection_abc import MateSelector
from genetic_llm.recombination_abc import RecombinerABC
from genetic_llm.evolution_abc import EvolutionEngineABC
from genetic_llm.evaluator_abc import EvaluatorABC  # pylint: disable=no-name-in-module

class EvolutionEngine(EvolutionEngineABC):
    def __init__(  # pylint: disable=too-many-arguments
        self, 
        config: GeneticConfig, 
        mate_selector: MateSelector,
        recombiner: RecombinerABC,
        evaluator: EvaluatorABC
    ):
        if config.elite_size > config.population_size:
            raise ValueError("Elite size cannot exceed population size")
        self.config = config
        self.mate_selector = mate_selector
        self.recombiner = recombiner
        self.evaluator = evaluator
        
    def evolve_population(self, population: list[Agent]) -> list[Agent]:
        self.evaluator.evaluate(population)
        
        elites = sorted(population, key=lambda x: x.fitness, reverse=True)[:self.config.elite_size]
        children = [
            Agent({
                ct: self.recombiner.combine(parent1.chromosomes[ct], parent2.chromosomes[ct])
                for ct in parent1.chromosomes.keys()
            })
            for _ in range(self.config.population_size - len(elites))
            for parent1, parent2 in [(self.mate_selector.select(population),
                                     self.mate_selector.select([a for a in population if a != parent1] or population))]
        ]
        for _ in range(num_children):
            parent1 = self.mate_selector.select(population)
            remaining = [a for a in population if a != parent1]
            parent2 = self.mate_selector.select(remaining if remaining else population)
            
            child_chromosomes = {
                ct: self.recombiner.combine(parent1.chromosomes[ct], parent2.chromosomes[ct])
                for ct in parent1.chromosomes.keys()
            }
            children.append(Agent(child_chromosomes))  # pylint: disable=abstract-class-instantiated
        
        return elites + children
# Package initialization
