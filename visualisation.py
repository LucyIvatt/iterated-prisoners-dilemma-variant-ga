import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import numpy as np


def init_figure(agents):
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

    agent_factions, agent_wealth = create_agents_array(agents)

    # Loop over data dimensions and create text annotations.
    for i in range(agent_factions.shape[0]):
        for j in range(agent_factions.shape[0]):
            text = ax.text(j, i, agent_wealth[i, j],
                           ha="center", va="center", color="black")

    colour_map = ListedColormap(["#FF9AA2", "#FFDAC1", "#B5EAD7", "#C7CEEA"])
    plt.imshow(agent_factions, cmap=colour_map)

    colours = [colour_map(i) for i in range(4)]
    labels = ['Saints', 'Buddies', 'Fight Club', 'Vandals']
    # create a patch (proxy artist) for every color
    patches = [mpatches.Patch(color=colours[i], label=labels[i])
               for i in range(4)]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)
    plt.show()


def update_figure(new_agents):
    agent_factions, agent_wealth = create_agents_array(new_agents)
    h.set_data(img)
    draw(), pause(1e-3)


def create_agents_array(agents):
    width = int(math.sqrt(len(agents)))
    agent_factions = np.zeros((width, width))
    agent_wealth = np.zeros((width, width))

    x = y = 0
    while y < width:
        for agent in agents:
            agent_factions[x][y] = agent.society.value
            agent_wealth[x][y] = agent.total_payoff
            x += 1
            if x == width:
                y += 1
                x = 0
    return agent_factions, agent_wealth
