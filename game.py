from enums import Society
import random
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches


class Agent():
    '''Represents a single agent within the model with their society assignment and total payoff. '''

    def __init__(self, unique_id, model):
        ''' Creates a new agent with a random society assignment and total payoff of 0'''
        self.global_model = model
        self.unique_id = unique_id
        self.total_payoff = 0
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

    @staticmethod
    def simulate_game(agent1, agent2):
        '''Calculates new total payoff depending on if each agent cooperates or is selfish'''
        if agent1.cooperates_with(agent2) and agent2.cooperates_with(agent1):
            agent1.total_payoff += 4
            agent2.total_payoff += 4
        elif agent1.cooperates_with(agent2) and not agent2.cooperates_with(agent1):
            agent2.total_payoff += 6
        elif not agent1.cooperates_with(agent2) and agent2.cooperates_with(agent1):
            agent1.total_payoff += 6
        else:
            agent1.total_payoff += 1
            agent2.total_payoff += 1


class GlobalModel():
    """Global model of the society simulation with N number of agents."""

    def __init__(self, num_agents, random_seed=None):
        self.num_agents = num_agents
        self.agents = []
        random.seed(random_seed)

        for i in range(self.num_agents):
            a = Agent(i, self)
            self.agents.append(a)

    def step(self):
        """Advance the model by one step."""
        agent1 = random.choice(self.agents)
        agent2 = random.choice(self.agents)

        # Ensures the same two agents are not picked
        while agent2 == agent1:
            agent2 = random.choice(self.agents)

        Agent.simulate_game(agent1, agent2)


model = GlobalModel(25, random_seed=50)
for i in range(200):
    model.step()

width = int(math.sqrt(len(model.agents)))
print(width)
agent_factions = np.zeros((width, width))
agent_wealth = np.zeros((width, width))

plt.rcParams.update({'font.size': 16})
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica']

fig = plt.figure()
fig.set_size_inches(8, 8)
fig.set_facecolor('#35455d')
fig.suptitle("Visualisation of Agent Faction Assignments",
             size=18, color="white", y=0.96)
ax = plt.gca()

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

x = y = 0
while y < width:
    for agent in model.agents:
        agent_factions[x][y] = agent.society.value
        agent_wealth[x][y] = agent.total_payoff
        x += 1
        if x == width:
            y += 1
            x = 0

# Loop over data dimensions and create text annotations.
for i in range(width):
    for j in range(width):
        text = ax.text(j, i, agent_wealth[i, j],
                       ha="center", va="center", color="black")

colormap = colors.ListedColormap(
    ["#FF9AA2", "#FFDAC1", "#B5EAD7", "#C7CEEA"])
plt.imshow(agent_factions, cmap=colormap)

colors = [colormap(i) for i in range(4)]
labels = ['Saints', 'Buddies', 'Fight Club', 'Vandals']
# create a patch (proxy artist) for every color
patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(4)]
# put those patched as legend-handles into the legend
plt.legend(handles=patches, loc='upper center', bbox_to_anchor=(0.5, -0.05),
           fancybox=True, shadow=True, ncol=5)
plt.show()
