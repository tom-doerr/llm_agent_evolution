import pytest
from genetic_llm.core.evaluators.string_optimizer import StringOptimizationEvaluator
from genetic_llm.core import GeneticConfig, Agent, ChromosomeType, Chromosome

class TestStringOptimizationEvaluator:
    @pytest.fixture
    def config(self):
        return GeneticConfig(
            max_length=23,
            fitness_weights={"a_score": 1.0, "length_penalty": -1.0}
        )

    def test_fitness_calculation(self, config):
        evaluator = StringOptimizationEvaluator(config)
        agent = Agent((  # pylint: disable=abstract-class-instantiated
            Chromosome(ChromosomeType.TASK, "aaaabaaa"),  # 7 a's
            Chromosome(ChromosomeType.MATE_SELECTION, "test"),
            Chromosome(ChromosomeType.RECOMBINATION, "test")
        ))
        
        evaluator.evaluate([agent])
        assert agent.fitness == pytest.approx((7 * 1.0) + (0 * -1.0))
        
    def test_length_penalty(self, config):
        evaluator = StringOptimizationEvaluator(config)
        agent = Agent((  # pylint: disable=abstract-class-instantiated
            Chromosome(ChromosomeType.TASK, "a" * 35),
            Chromosome(ChromosomeType.MATE_SELECTION, "test"),
            Chromosome(ChromosomeType.RECOMBINATION, "test")
        ))
        
        evaluator.evaluate([agent])
        assert agent.fitness == pytest.approx(35.0 - 12.0)  # 35 a's (1.0 each), 12 over limit (-1.0 each)
        
    def test_initial_generation(self, config):
        evaluator = StringOptimizationEvaluator(config)
        initial = evaluator.generate_initial()
        assert 15 <= len(initial.value) <= 30
        assert any(c == 'a' for c in initial.value.lower())
        assert initial.type == ChromosomeType.TASK

    def test_mutation(self, config):
        evaluator = StringOptimizationEvaluator(config)
        original = Chromosome(ChromosomeType.TASK, "aaaaaaaaaa")
        
        # Test with high mutation rate
        mutated = evaluator.mutate(original, 0.8)
        assert mutated.value != original.value
        assert len(mutated.value) >= 9  # Allow length changes
        
        # Test type preservation
        assert mutated.type == ChromosomeType.TASK
