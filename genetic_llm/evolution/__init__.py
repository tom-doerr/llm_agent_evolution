from typing import List
from .core import Agent, GeneticConfig
from genetic_llm.mate_selection_abc import MateSelector
from genetic_llm.recombination_abc import RecombinerABC

class EvolutionEngine:
    def __init__(self, config: GeneticConfig, 
                 mate_selector: MateSelector,
                 recombiner: RecombinerABC):
        self.config = config
        self.mate_selector = mate_selector
        self.recombiner = recombiner
        
    def evolve_population(self, population: List[Agent]) -> List[Agent]:
        new_population = []
        
        # Elitism
        elites = sorted(population, key=lambda x: x.fitness, reverse=True)[:self.config.elite_size]
        new_population.extend(elites)
        
        # Breed new agents
        while len(new_population) < self.config.population_size:
            parent1 = self.mate_selector.select(population)
            parent2 = self.mate_selector.select(population)
            
            child_chromosomes = {}
            for ct in parent1.chromosomes:
                child_chromosomes[ct] = self.recombiner.combine(
                    parent1.chromosomes[ct],
                    parent2.chromosomes[ct]
                )
                
            new_population.append(Agent(child_chromosomes))
            
        return new_population
