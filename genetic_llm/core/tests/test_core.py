import pytest
from ..core import Agent, ChromosomeType, Chromosome
from genetic_llm.core_abc import AgentABC

class TestAgent:
    def test_implements_abc(self):
        assert issubclass(Agent, AgentABC)
    def test_agent_creation_with_valid_chromosomes(self):
        agent = Agent((
            Chromosome(ChromosomeType.TASK, "test"),
            Chromosome(ChromosomeType.MATE_SELECTION, "test"),
            Chromosome(ChromosomeType.RECOMBINATION, "test")
        ))
        assert agent.fitness == 0.0
        assert len(agent.chromosomes) == 3

    def test_agent_requires_all_chromosome_types(self):
        with pytest.raises(ValueError):
            Agent((
                Chromosome(ChromosomeType.TASK, "test"),
                Chromosome(ChromosomeType.MATE_SELECTION, "test")
            ))

    def test_fitness_validation(self):
        valid_chromosomes = (
            Chromosome(ChromosomeType.TASK, "t"),
            Chromosome(ChromosomeType.MATE_SELECTION, "ms"),
            Chromosome(ChromosomeType.RECOMBINATION, "r"),
        )
        
        with pytest.raises(ValueError):
            Agent(valid_chromosomes, fitness=-0.1)
            
        with pytest.raises(ValueError):
            Agent(valid_chromosomes, fitness=1.1)

    def test_duplicate_chromosome_types(self):
        with pytest.raises(ValueError):
            Agent((
                Chromosome(ChromosomeType.TASK, "t1"),
                Chromosome(ChromosomeType.TASK, "t2"),
                Chromosome(ChromosomeType.MATE_SELECTION, "ms"),
                Chromosome(ChromosomeType.RECOMBINATION, "r"),
            ))

    def test_repr_representation(self):
        agent = Agent((
            Chromosome(ChromosomeType.TASK, "t"),
            Chromosome(ChromosomeType.MATE_SELECTION, "ms"),
            Chromosome(ChromosomeType.RECOMBINATION, "r"),
        ), fitness=0.75)
        
        assert "fitness=0.75" in repr(agent)
        assert "TASK" in repr(agent)
        assert "MATE_SELECTION" in repr(agent)
        assert "RECOMBINATION" in repr(agent)

class TestChromosome:
    def test_creation(self):
        ct = ChromosomeType.TASK
        c = Chromosome(ct, "test_value")
        assert c.type == ct
        assert c.value == "test_value"
        
    def test_invalid_type(self):
        with pytest.raises(TypeError):
            Chromosome("not_enum", "value")
