from .mutation_operator_abc import MutationOperatorABC

class BasicMutationOperator(MutationOperatorABC):
    def mutate(self, chromosome: str, mutation_rate: float) -> str:
        """Simple mutation that appends '[M]' with probability mutation_rate"""
        import random
        if random.random() < mutation_rate:
            return chromosome + "[M]"
        return chromosome
