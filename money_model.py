from mesa import Agent, Model
from enums import Society
import random


class MoneyAgent(Agent):
    '''An agent with a starting wealth of 0 and a randomly assigned society'''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.total_payoff = 0
        self.society = random.choice(list(Society))

    def __str__(self):
        return f"Agent {self.unique_id} - Society = {self.society.name}, Total Payoff = {self.total_payoff}"

    def step(self):
        # The agent's step will go here.
        print(str(self))


class GlobalModel(Model):
    """Global model of the society simulation with N number of agents."""

    def __init__(self, num_agents):
        self.num_agents = num_agents
        # self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            print(a)

    def step(self):
        """Advance the model by one step."""
        # self.schedule.step()


global_model = GlobalModel(10)
