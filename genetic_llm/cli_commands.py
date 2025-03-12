"""CLI command implementations isolated from core logic"""
import click
from genetic_llm.core import GeneticConfig, Agent, ChromosomeType
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.evolution import EvolutionEngine

def evolve_command(generations: int, config: GeneticConfig):
    """Execute evolution process with configured components"""
    mate_selector = DSPyMateSelector()
    recombiner = DSPyRecombiner()
    engine = EvolutionEngine(config, mate_selector, recombiner)
    
    population = _init_population(config)
    
    for gen in range(generations):
        population = engine.evolve_population(population)
        click.echo(f"Generation {gen+1} completed")
    
    return population

def _init_population(config: GeneticConfig):
    """Initialize population with random chromosomes"""
    return [
        Agent({
            ChromosomeType.TASK: f"Do X using {random.choice(['method A', 'method B'])}",
            ChromosomeType.MATE_SELECTION: f"Select mates based on {random.choice(['fitness', 'diversity'])}",
            ChromosomeType.RECOMBINATION: f"Combine using {random.choice(['crossover', 'blending'])}"
        }) for _ in range(config.population_size)
    ]
