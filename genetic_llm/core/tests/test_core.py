import pytest
from genetic_llm.core import Agent, ChromosomeType, Chromosome
from genetic_llm.core_abc import AgentABC

class TestAgent:  # pylint: disable=too-many-public-methods
    def test_implements_abc(self):
        assert issubclass(Agent, AgentABC)
        assert 'select_mates' in Agent.__abstractmethods__
        assert 'recombine' in Agent.__abstractmethods__
    def test_agent_creation_with_valid_chromosomes(self):
        agent = Agent((  # pylint: disable=abstract-class-instantiated
            Chromosome(ChromosomeType.TASK, "test"),
            Chromosome(ChromosomeType.MATE_SELECTION, "test"),
            Chromosome(ChromosomeType.RECOMBINATION, "test")
        ))
        assert agent.fitness == 0.0
        assert len(agent.chromosomes) == 3

    def test_agent_requires_all_chromosome_types(self):
        with pytest.raises(ValueError):
            Agent((  # pylint: disable=abstract-class-instantiated
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
            Agent(valid_chromosomes, fitness=-0.1)  # pylint: disable=abstract-class-instantiated
            
        with pytest.raises(ValueError):
            Agent(valid_chromosomes, fitness=1.1)  # pylint: disable=abstract-class-instantiated

    def test_duplicate_chromosome_types(self):
        with pytest.raises(ValueError):
            Agent((  # pylint: disable=abstract-class-instantiated
                Chromosome(ChromosomeType.TASK, "t1"),
                Chromosome(ChromosomeType.TASK, "t2"),
                Chromosome(ChromosomeType.MATE_SELECTION, "ms"),
                Chromosome(ChromosomeType.RECOMBINATION, "r"),
            ))

    def test_repr_representation(self):
        agent = Agent((  # pylint: disable=abstract-class-instantiated
            Chromosome(ChromosomeType.TASK, "t"),
            Chromosome(ChromosomeType.MATE_SELECTION, "ms"),
            Chromosome(ChromosomeType.RECOMBINATION, "r"),
        ), fitness=0.75)
        
        assert "fitness=0.75" in repr(agent)
        assert "TASK" in repr(agent)
        assert "MATE_SELECTION" in repr(agent)
        assert "RECOMBINATION" in repr(agent)

    def test_genetic_operations(self):
        parent1 = Agent((  # pylint: disable=abstract-class-instantiated
            Chromosome(ChromosomeType.TASK, "aaaa"),
            Chromosome(ChromosomeType.MATE_SELECTION, "tournament_selection"),
            Chromosome(ChromosomeType.RECOMBINATION, "single_point_crossover"),
        ))
        parent2 = Agent((  # pylint: disable=abstract-class-instantiated
            Chromosome(ChromosomeType.TASK, "bbbb"),
            Chromosome(ChromosomeType.MATE_SELECTION, "tournament_selection"),
            Chromosome(ChromosomeType.RECOMBINATION, "single_point_crossover"),
        ))
        
        child = parent1.recombine(parent2)
        assert len(child.chromosomes[0].value) == 4
        assert child.fitness == 0.0

class TestChromosome:
    def test_creation(self):
        ct = ChromosomeType.TASK
        c = Chromosome(ct, "test_value")
        assert c.type == ct
        assert c.value == "test_value"
        
    def test_invalid_type(self):
        with pytest.raises(TypeError):
            Chromosome("not_enum", "value")
