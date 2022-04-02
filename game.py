from enums import Society
import random
import numpy as np
from visualisation import init_visualisation, create_agents_arrays, update_visualisation
import time
from statistics import median
from collections import Counter
import itertools
import logging

lookup_dict = {y: x for x, y in dict(
    enumerate(itertools.product(["S", "B", "F", "V"], repeat=4))).items()}


class Agent():
    '''Represents a single agent within the model with their society assignment and total payoff. '''

    def __init__(self, unique_id, chromosome):
        ''' Creates a new agent with a random society assignment and total payoff of 0'''
        self.unique_id = unique_id
        self.chromosome = chromosome
        self.reset()

    def __str__(self):
        '''Returns an agents ID, society and total payoff'''
        return f"Agent {self.unique_id} - ({self.society.name=}, {self.total_payoff=}, {self.rounds_played=}, {self.history=}, {self.fitness()=}\n{self.chromosome[:10]})"

    def cooperates_with(self, agent):
        '''Determines if the agent will cooperate with a specified agent depending on both of their society assignments'''

        if self.society == Society.SAINTS:
            return True  # Saints always cooperate with everyone
        elif self.society == Society.BUDDIES and agent.society == Society.BUDDIES:
            return True  # Buddies only cooperate with buddies
        elif self.society == Society.FIGHT_CLUB and agent.society != Society.FIGHT_CLUB:
            return True  # Fight club only cooperate with people outside of fight club
        else:
            # Otherwise no cooperation (includes vandals who never cooperate)
            return False

    def change_society(self):
        '''Uses the base 4 value of the play history to get the index to lookup which society to switch to from the chromosome'''
        index = lookup_dict[tuple(self.history)]
        if self.chromosome[index] == 0:
            self.society = random.choice(list(Society))

    def update_score(self, value):
        self.total_payoff += value
        self.rounds_played += 1

    def update_history(self, opponent):
        new_match = [self.society.value, opponent.society.value]
        self.history = self.history[2:4] + new_match

    def fitness(self):
        if self.rounds_played != 0:
            return self.total_payoff / self.rounds_played
        else:
            return 0

    def reset(self):
        self.total_payoff = 0
        self.rounds_played = 0
        self.society = random.choice(list(Society))
        self.history = [random.choice(["S", "B", "F", "V"]) for i in range(4)]


class Simulator():
    """Global model of the society simulation with N number of agents."""

    def __init__(self, agents, headless=True):

        self.agents = agents
        self.headless = headless
        if not headless:
            self.display_fig, self.display_im = init_visualisation(self.agents)

    def step(self):
        """Advance the model by one step."""
        agent1 = random.choice(self.agents)
        agent2 = random.choice(self.agents)

        # Ensures the same two agents are not picked
        while agent2 == agent1:
            agent2 = random.choice(self.agents)

        if not self.headless:
            update_visualisation(
                self.display_fig, self.display_im, self.agents)

        self.play_round(agent1, agent2)

        if not self.headless:
            time.sleep(0.05)

    def run(self, n):
        for i in range(n):
            self.step()

    def reset_agents(self):
        for agent in self.agents:
            agent.reset()

    def get_stats(self):
        agent_fitnesses = [agent.fitness() for agent in self.agents]
        max_fitness = max(agent_fitnesses)
        mean_fitness = sum(agent_fitnesses) / len(agent_fitnesses)
        min_fitness = min(agent_fitnesses)
        median_fitness = median(agent_fitnesses)

        return {"min": min_fitness, "mean": mean_fitness, "median": median_fitness, "max": max_fitness}

    def get_counts(self):
        assignments = [agent.society for agent in self.agents]
        return Counter(assignments)

    @ staticmethod
    def play_round(agent1, agent2):
        '''Calculates new total payoff depending on if each agent cooperates or is selfish'''
        if agent1.cooperates_with(agent2) and agent2.cooperates_with(agent1):
            agent1.update_score(4)
            agent2.update_score(4)
        elif agent1.cooperates_with(agent2) and not agent2.cooperates_with(agent1):
            agent1.update_score(0)
            agent2.update_score(6)
        elif not agent1.cooperates_with(agent2) and agent2.cooperates_with(agent1):
            agent1.update_score(6)
            agent2.update_score(0)
        else:
            agent1.update_score(1)
            agent2.update_score(1)

        agent1.update_history(agent2)
        agent2.update_history(agent1)

        agent1.change_society()
        agent2.change_society()
