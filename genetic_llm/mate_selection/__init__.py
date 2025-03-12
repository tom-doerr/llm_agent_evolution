# pylint: disable=too-many-lines
import logging
import threading
import time
import dspy
from typing import Optional
from genetic_llm.core import Agent
from genetic_llm.config import MateSelectionConfig
from .mate_selection_abc import MateSelector

logger = logging.getLogger(__name__)

class SelectionTimeoutError(Exception):
    """Custom timeout exception for selection operations"""

def timeout_wrapper(func, timeout, params):
    """Cross-platform timeout decorator implementation
    Args:
        func: Callable to execute
        timeout: Maximum execution time in seconds
        params: Tuple containing (args_tuple, kwargs_dict)
    """
    args, kwargs = params
    outcome = {'result': None, 'error': None}
    
    def worker():
        try:
            outcome['result'] = func(*args, **(kwargs or {}))
        except (ValueError, IndexError, TimeoutError) as e:
            outcome['error'] = e
    
    thread = threading.Thread(target=worker)
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive() or not outcome['result']:
        raise SelectionTimeoutError(f"Timeout after {timeout} seconds")
    
    if outcome['error']:
        raise outcome['error']
    
    return outcome['result']

class DSPyMateSelector(MateSelector, dspy.Module):
    def _get_population_data(self, population: list[Agent]) -> dict:
        """Validate and extract population data for model input."""
        chromosomes = []
        fitness = []
        for agent in population:
            if not hasattr(agent, 'fitness') or agent.fitness is None:
                raise ValueError(f"Agent {agent} missing required fitness value")
            chromosomes.append(agent.chromosomes)
            fitness.append(agent.fitness)
        
        return {
            "population_chromosomes": chromosomes,
            "population_fitness": fitness
        }
    def __init__(self, config: Optional[MateSelectionConfig] = None):
        super().__init__()
        self.config = config or MateSelectionConfig()
        self._setup_logging()
        self._init_model()

    def _setup_logging(self):
        logger.setLevel(self.config.log_level)

    def _init_model(self):
        self.lm = dspy.LM(self.config.model_name)
        self.select_mate = dspy.Predict(
            "population_chromosomes, population_fitness -> selected_index",
            instructions=(
                "Select the 0-based integer index of the most promising agent. "
                "Your response MUST be a single integer between 0 and {population_size-1}. "
                "Non-integer responses will cause system errors."
            )
        )


    def _validate_index(self, raw_index: str, population_size: int) -> int:  # pylint: disable=too-many-locals
        try:
            index_float = float(raw_index.strip())
            if abs(index_float - round(index_float)) > self.config.require_integer_threshold:
                raise ValueError(f"Index {index_float} is not close enough to integer")
                
            index = int(round(index_float))
        except (ValueError, TypeError) as e:
            logger.error("Invalid index conversion: %s", raw_index)
            raise ValueError(f"Invalid index format: {raw_index}") from e

        if not 0 <= index < population_size:
            logger.error("Index out of bounds: %d (population size %d)", index, population_size)
            raise IndexError(f"Index {index} out of range [0-{population_size-1}]")
            
        return index

    def select(self, population: list[Agent]) -> Agent:
        if not population:
            logger.error("Selection attempted with empty population")
            raise ValueError("Cannot select from empty population")

        pop_data = self._get_population_data(population)
        attempts = 0
        
        while True:
            try:
                return timeout_wrapper(
                    self._execute_selection, 
                    self.config.timeout_seconds,
                    (pop_data, len(population))
                )
            except (SelectionTimeoutError, ValueError, IndexError) as e:
                attempts += 1
                if attempts >= self.config.max_retries:
                    logger.error("Selection failed after %d attempts", attempts)
                    raise
                logger.warning("Selection attempt %d failed: %s", attempts, str(e))
                time.sleep(self.config.retry_delay * (2 ** (attempts-1)))

    def _execute_selection(self, pop_data, population_size):
        """Core selection logic without timeout handling"""
        with dspy.context(lm=self.lm):
            prediction = self.select_mate(**pop_data)
        
        logger.debug("Raw model response: %s", prediction.selected_index)
        return self.population[self._validate_index(prediction.selected_index, population_size)]
# Package initialization
