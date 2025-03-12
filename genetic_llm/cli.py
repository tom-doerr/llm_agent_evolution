import click
from .evolution import EvolutionEngine
from .core import GeneticConfig, Agent, ChromosomeType
import random

@click.group()
def main():
    """Genetic LLM Agent Evolution CLI"""
    
@main.command()
@click.option("--generations", default=100, help="Number of generations to evolve")
def evolve(generations):
    config = GeneticConfig()
    # Inject implementations
    mate_selector = MateSelector()
    recombiner = Recombiner()
    engine = EvolutionEngine(config, mate_selector, recombiner)
    
    # Initialize random population
    population = [
        Agent({
            ChromosomeType.TASK: f"Do X using {random.choice(['method A', 'method B'])}",
            ChromosomeType.MATE_SELECTION: f"Select mates based on {random.choice(['fitness', 'diversity'])}",
            ChromosomeType.RECOMBINATION: f"Combine using {random.choice(['crossover', 'blending'])}"
        }) for _ in range(config.population_size)
    ]
    
    for gen in range(generations):
        population = engine.evolve_population(population)
        # Evaluate fitness here
        click.echo(f"Generation {gen+1} completed")
