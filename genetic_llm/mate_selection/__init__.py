import dspy

class MateSelector(dspy.Module):
    def __init__(self):
        super().__init__()
        self.lm = dspy.LM('openrouter/google/gemini-2.0-flash-001')
        self.select_mate = dspy.Predict("agent_chromosomes, population_fitness -> selected_mate")

    def forward(self, agent, population):
        return self.select_mate(
            agent_chromosomes=agent.chromosomes,
            population_fitness=[a.fitness for a in population]
        )
