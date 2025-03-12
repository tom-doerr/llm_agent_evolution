import pytest
from genetic_llm.core import Agent, Chromosome, ChromosomeType

def test_valid_agent_creation():
    chromosomes = (
        Chromosome(type=ChromosomeType.TASK, value="Solve math problems"),
        Chromosome(type=ChromosomeType.MATE_SELECTION, value="Top 10% selection")
    )
    agent = Agent(chromosomes, fitness=0.75)
    assert agent.fitness == 0.75
    assert len(agent.chromosomes) == 2

def test_duplicate_chromosome_types():
    chromosomes = (
        Chromosome(type=ChromosomeType.TASK, value="Task 1"),
        Chromosome(type=ChromosomeType.TASK, value="Task 2")
    )
    with pytest.raises(ValueError, match="Duplicate chromosome types"):
        Agent(chromosomes)

def test_invalid_fitness_values():
    chromosomes = (Chromosome(type=ChromosomeType.TASK, value="Valid"),)
    
    with pytest.raises(ValueError, match="Fitness must be between 0.0-1.0"):
        Agent(chromosomes, fitness=-0.1)
        
    with pytest.raises(ValueError, match="Fitness must be between 0.0-1.0"):
        Agent(chromosomes, fitness=1.1)

def test_empty_chromosomes():
    with pytest.raises(ValueError, match="Must provide at least one chromosome"):
        Agent(())
