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
                ct: self.recombiner.combine(p1.chromosomes[ct], p2.chromosomes[ct])
                for ct, p1, p2 in zip(parents[0].chromosomes, parents, parents[1:])
            }
            children.append(Agent(child_chromosomes))
        
        new_population = elites + children
        return new_population
# Package initialization
