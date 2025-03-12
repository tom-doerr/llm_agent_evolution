import pytest
from genetic_llm.core import Agent, ChromosomeType
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
