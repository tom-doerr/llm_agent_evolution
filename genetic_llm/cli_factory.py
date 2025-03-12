"""Factory for creating CLI components with proper isolation"""
from genetic_llm.mate_selection import DSPyMateSelector
from genetic_llm.recombination import DSPyRecombiner
from genetic_llm.evolution import EvolutionEngine
from genetic_llm.core import GeneticConfig

def create_evolution_engine(config: GeneticConfig) -> EvolutionEngine:
    """Create evolution engine with default components"""
    return EvolutionEngine(
        config=config,
        mate_selector=DSPyMateSelector(),
        recombiner=DSPyRecombiner()
    )
