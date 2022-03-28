from enums import Society
import random
import numpy as np
from visualisation import init_visualisation, create_agents_arrays, update_visualisation
import time


class Agent():
    '''Represents a single agent within the model with their society assignment and total payoff. '''

    def __init__(self, unique_id, model):
        ''' Creates a new agent with a random society assignment and total payoff of 0'''
        self.global_model = model
        self.unique_id = unique_id
        self.total_payoff = 0
        self.average_payoff = 0
        self.rounds_played = 0
        self.society = random.choice(list(Society))

    def __str__(self):
        '''Returns an agents ID, society and total payoff'''
        return f"Agent {self.unique_id} - ({self.society.name}, {self.total_payoff})"

    def cooperates_with(self, agent):
        '''Determines if the agent will cooperate with a specified agent depending on both of their society assignments'''

        # Saints always cooperate with everyone
        if self.society == Society.SAINTS:
            return True
        # Buddies only cooperate with buddies
        elif self.society == Society.BUDDIES and agent.society == Society.BUDDIES:
            return True
        # Fight club only coperate with people outside of fight club
        elif self.society == Society.FIGHT_CLUB and agent.society != Society.FIGHT_CLUB:
            return True
        # Otherwise no cooperation (includes vandals who never cooperate)
        else:
            return False

    def change_society(self, agent):
        '''When given the other players total wealth and society assignment, the agent can decide to switch societies'''
        # Add code for society switching here, will

        # will access the lookup table to get the index, then use this index to pick the value from the strategy
        self.society = random.choice(list(Society))

    def update_score(self, value):
        self.total_payoff += value
        self.rounds_played += 1
        if self.total_payoff != 0:
            self.average_payoff = self.total_payoff / self.rounds_played

    @staticmethod
    def simulate_game(agent1, agent2):
        '''Calculates new total payoff depending on if each agent cooperates or is selfish'''
        if agent1.cooperates_with(agent2) and agent2.cooperates_with(agent1):
            agent1.update_score(4)
            agent2.update_score(4)
        elif agent1.cooperates_with(agent2) and not agent2.cooperates_with(agent1):
            agent1.update_score(0)
            agent2.update_score(6)
        elif not agent1.cooperates_with(agent2) and agent2.cooperates_with(agent1):
            agent1.update_score(6)
        else:
            agent1.update_score(1)
            agent2.update_score(1)


class GlobalModel():
    """Global model of the society simulation with N number of agents."""

    def __init__(self, num_agents, headless=True, random_seed=None):
        random.seed(random_seed)

        self.num_agents = num_agents
        self.agents = []
        self.headless = headless

        for i in range(self.num_agents):
            a = Agent(i, self)
            self.agents.append(a)

        if not headless:
            self.display_fig, self.display_im = init_visualisation(self.agents)

    def step(self):
        """Advance the model by one step."""
        agent1 = random.choice(self.agents)
        agent2 = random.choice(self.agents)

        # Ensures the same two agents are not picked
        while agent2 == agent1:
            agent2 = random.choice(self.agents)

        Agent.simulate_game(agent1, agent2)

        agent1.change_society(agent2)
        agent2.change_society(agent1)

        if not self.headless:
            update_visualisation(
                self.display_fig, self.display_im, self.agents)

    def run_simulation(self, n):
        for agent in self.agents:
            print(agent)
        print("----------------")
        for _ in range(n):
            self.step()
            for agent in self.agents:
                print(agent)
            print("----------------")
            time.sleep(30)


model = GlobalModel(25, headless=False, random_seed=50)
model.run_simulation(2000)


# Notes for next time
# Create a lookup table for the history string comparisons (4^6 if doing memory-3), something like -
# enumerate(itertools.product(list(Society), repeat=6))
# will need to switch it so the index isnt the key and is instead the value i.e.
# for i v, make it v i

# Agent:
# History (e.g. last 3 games) length 6 - BBVSFB
# Strategy (Chromosome) - length of 4^6 with evolving outputs for the lookup table (BVFBSFSBFB....)
# will use index from lookup table to get the gene which relates to the 'learned' choice to switch society
