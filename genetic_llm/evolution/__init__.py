from genetic_llm.core import Agent, GeneticConfig
from genetic_llm.core_abc import AgentABC
from genetic_llm.mate_selection_abc import MateSelector
from genetic_llm.recombination_abc import RecombinerABC
from genetic_llm.evolution_abc import EvolutionEngineABC
from genetic_llm.evaluator_abc import EvaluatorABC  # pylint: disable=no-name-in-module

class EvolutionEngine(EvolutionEngineABC):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        config: GeneticConfig, 
        mate_selector: MateSelector,
        recombiner: RecombinerABC,
        evaluator: EvaluatorABC,
        mutation_operator: MutationOperatorABC,
        chromosome_validator: ChromosomeValidatorABC  # New parameter
    ):
        if config.elite_size > config.population_size:
            raise ValueError("Elite size cannot exceed population size")
        self.config = config
        self.mate_selector = mate_selector
        self.recombiner = recombiner
        self.evaluator = evaluator
        self.mutation_operator = mutation_operator
        self.validator = chromosome_validator  # New field
        
    def evolve_population(self, population: list[Agent]) -> list[Agent]:  # pylint: disable=too-many-locals
        self.evaluator.evaluate(population)
        
        # Validate existing population first
        for agent in population:
            self.validator.validate(agent.chromosomes)

        elites = sorted(population, key=lambda x: x.fitness, reverse=True)[:self.config.elite_size]
        children = []
        
        # Calculate exact number of children needed
        num_children = self.config.population_size - len(elites)
        
        for _ in range(num_children):
            parent1 = self.mate_selector.select(population)
            remaining = [a for a in population if a != parent1]
            
            # Ensure we don't try to select from empty list
            parent2_source = remaining if remaining else population
            parent2 = self.mate_selector.select(parent2_source)
            
            child_chromosomes = {
                ct: self.mutation_operator.mutate(
                    self.recombiner.combine(parent1.chromosomes[ct], parent2.chromosomes[ct]),
                    self.config.mutation_rate
                )
                for ct in parent1.chromosomes.keys()
            }
            
            self.validator.validate(child_chromosomes)  # Validate new children
            children.append(Agent(child_chromosomes))  # pylint: disable=abstract-class-instantiated
        return elites + children
# Package initialization
