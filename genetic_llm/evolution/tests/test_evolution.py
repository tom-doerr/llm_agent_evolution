import pytest
from unittest.mock import Mock
from genetic_llm.evolution import EvolutionEngine
from genetic_llm.core import GeneticConfig, ChromosomeType
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.evolution_abc import EvolutionEngineABC

# Test concrete implementation
class TestConcreteEvolutionEngine(EvolutionEngine):
    """Concrete implementation for testing abstract base class functionality""" 

# Test double for abstract Agent class
class TestAgent:
    def __init__(self, chromosomes, fitness=0):
        self.chromosomes = chromosomes
        self.fitness = fitness

class TestEvolutionEngineBasics:
    def test_implements_abc(self):
        assert issubclass(EvolutionEngine, EvolutionEngineABC)
    def test_evolve_population_size_remains_constant(self):
        config = GeneticConfig(population_size=10, elite_size=2)
        engine = TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
            config, DSPyMateSelector(), DSPyRecombiner(), Mock(), Mock()  # pylint: disable=abstract-class-instantiated
        )
        population = [TestAgent({ct: "test" for ct in ChromosomeType}) for _ in range(10)]
        new_pop = engine.evolve_population(population)
        assert len(new_pop) == config.population_size
    
    def test_elites_are_preserved(self):
        config = GeneticConfig(population_size=10, elite_size=2)
        engine = TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
            config, DSPyMateSelector(), DSPyRecombiner(), Mock(), Mock()
        )
        
        # Create population with ascending fitness
        population = [TestAgent({ct: str(i) for ct in ChromosomeType}, fitness=i) for i in range(10)]
        new_pop = engine.evolve_population(population)
        
        # Top 2 should be highest fitness agents
        assert new_pop[0].fitness == 9
        assert new_pop[1].fitness == 8
    
    def test_invalid_elite_size_raises_error(self):
        config = GeneticConfig(population_size=5, elite_size=10)
        with pytest.raises(ValueError, match="Elite size cannot exceed population size"):
            TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
                config, DSPyMateSelector(), DSPyRecombiner(), Mock()
            )

    def test_tied_fitness_elite_selection(self):
        # Add mock mutation operator to constructor
        engine = TestConcreteEvolutionEngine(
            GeneticConfig(population_size=5, elite_size=2), 
            DSPyMateSelector(), 
            DSPyRecombiner(), 
            Mock(),
            Mock()
        )
        config = GeneticConfig(population_size=5, elite_size=2)
        engine = TestConcreteEvolutionEngine(  # pylint: disable=abstract-class-instantiated
            config, DSPyMateSelector(), DSPyRecombiner(), Mock(), Mock()
        )
        
        population = [
            TestAgent({"dna": "A"}, fitness=10),
            TestAgent({"dna": "B"}, fitness=10),  # Tie for first
            TestAgent({"dna": "C"}, fitness=5),
            TestAgent({"dna": "D"}, fitness=5),
            TestAgent({"dna": "E"}, fitness=1)
        ]
        new_pop = engine.evolve_population(population)
        
        # Should preserve both top 10 fitness agents
        assert sum(1 for a in new_pop if a.fitness == 10) == 2


    def test_mutation_applied_to_children(self):
        config = GeneticConfig(population_size=3, elite_size=1, mutation_rate=1.0)
        mutation_mock = Mock(side_effect=lambda x, _: x + "_mutated")
        engine = TestConcreteEvolutionEngine(
            config, Mock(), Mock(), Mock(), mutation_mock
        )
        
        population = [
            TestAgent({"dna": "A"}, fitness=10),
            TestAgent({"dna": "B"}, fitness=5),
            TestAgent({"dna": "C"}, fitness=1)
        ]
        
        new_pop = engine.evolve_population(population)
        child = next(a for a in new_pop if a not in population[:1])  # Skip elite
        assert "_mutated" in child.chromosomes["dna"]

    def test_chromosome_validation():
        from genetic_llm.validation import JSONSchemaValidator
        
        schemas = {
            "dna": {
                "type": "object",
                "properties": {
                    "sequence": {"type": "string"},
                    "length": {"type": "number"}
                },
                "required": ["sequence"]
            }
        }
        validator = JSONSchemaValidator(schemas)
        
        # Valid case
        valid_agent = TestAgent({"dna": '{"sequence": "ATCG", "length": 4}'})
        assert validator.validate(valid_agent.chromosomes) is True
        
        # Invalid JSON
        invalid_json_agent = TestAgent({"dna": "{bad json}"})
        with pytest.raises(ValueError):
            validator.validate(invalid_json_agent.chromosomes)
            
        # Missing required field
        invalid_schema_agent = TestAgent({"dna": '{"length": 4}'})
        with pytest.raises(ValueError):
            validator.validate(invalid_schema_agent.chromosomes)

    def test_evolution_engine_validates_population():
        mock_validator = Mock()
        engine = TestConcreteEvolutionEngine(
            GeneticConfig(population_size=10, elite_size=2),
            Mock(), Mock(), Mock(), Mock(),
            mock_validator
        )
        
        population = [TestAgent({ct: "{}" for ct in ChromosomeType}) for _ in range(10)]
        engine.evolve_population(population)
        
        assert mock_validator.validate.call_count == len(population) + 8  # 10 existing + 8 new children

    def test_mutation_rate_respected(self):
        config = GeneticConfig(population_size=10, elite_size=2, mutation_rate=0.0)
        mutation_mock = Mock(return_value="mutated")
        engine = TestConcreteEvolutionEngine(
            config, Mock(), Mock(), Mock(), mutation_mock
        )
        
        population = [TestAgent({ct: "orig" for ct in ChromosomeType}) for _ in range(10)]
        engine.evolve_population(population)
        mutation_mock.assert_not_called()
