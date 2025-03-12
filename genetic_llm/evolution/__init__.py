from typing import List
from .core import Agent, GeneticConfig
from genetic_llm.mate_selection_abc import MateSelector
from genetic_llm.recombination_abc import RecombinerABC

from genetic_llm.evolution_abc import EvolutionEngineABC

class EvolutionEngine(EvolutionEngineABC):
    def __init__(self, config: GeneticConfig, 
                 mate_selector: MateSelector,
                 recombiner: RecombinerABC):
        self.config = config
        self.mate_selector = mate_selector
        self.recombiner = recombiner
        
    def evolve_population(self, population: list[Agent]) -> list[Agent]:
        # First evaluate current population's fitness
        from genetic_llm.core.evaluators.string_optimizer import StringOptimizationEvaluator
        evaluator = StringOptimizationEvaluator(self.config)
        evaluator.evaluate(population)
        if self.config.elite_size > self.config.population_size:
            raise ValueError("Elite size cannot exceed population size")
            
        # Preserve top performers
        elites = sorted(population, key=lambda x: x.fitness, reverse=True)[:self.config.elite_size]
        
        # Generate offspring to fill remaining slots
        num_children = self.config.population_size - len(elites)
        children = []
        for _ in range(num_children):
            parents = [self.mate_selector.select(population) for _ in range(2)]
            child_chromosomes = {
                ct: self.recombiner.combine(parents[0].chromosomes[ct], parents[1].chromosomes[ct])
                for ct in parents[0].chromosomes  # Use first parent's chromosome types
            }
            children.append(Agent(child_chromosomes))
        
        new_population = elites + children
        return new_population
# Package initialization
