import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import numpy as np
import time


def init_visualisation(agents):
    '''Creates the original visualisation to show agents factions & current wealth'''
    # Turns interactive mode on to allow for updates
    plt.ion()

    # Sets the default font and size
    plt.rcParams.update({'font.size': 16})
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Helvetica']

    # Sets up the figure, title and background colour
    fig = plt.figure()
    fig.set_size_inches(8, 8)
    fig.set_facecolor('#35455d')
    fig.suptitle("Visualisation of Agent Faction Assignments",
                 size=18, color="white", y=0.96)

    # Hides the tick labels and sets ticks to be white
    ax = plt.gca()
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    agent_factions, agent_wealth = create_agents_arrays(agents)

    # Loop over array and create text annotations.
    for i in range(agent_factions.shape[0]):
        for j in range(agent_factions.shape[1]):
            ax.text(j, i, agent_wealth[i, j],
                    ha="center", va="center", color="black")

    # Manually defines the colours for each faction and plots the array
    colour_map = ListedColormap(["#FF9AA2", "#FFDAC1", "#B5EAD7", "#C7CEEA"])
    im = plt.imshow(agent_factions, cmap=colour_map)

    # Manually defines the key underneath the visualisation to map each colour to a faction
    colours = [colour_map(i) for i in range(4)]
    labels = ['Saints', 'Buddies', 'Fight Club', 'Vandals']
    patches = [mpatches.Patch(color=colours[i], label=labels[i])
               for i in range(4)]
    plt.legend(handles=patches, loc='upper center', bbox_to_anchor=(0.5, -0.05),
               fancybox=True, shadow=True, ncol=5)

    # Updates and shows the figure
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.show()

    return fig, im


def create_agents_arrays(agents):
    '''Creates two square arrays. One containing a value for each agents faction assignment -SAINTS = 1
    BUDDIES = 2, FIGHT_CLUB = 3 & VANDALS = 4. The second contains the wealth of each of these agents. Due to 
    positioning not being a factor, agents are placed arbitrarily.'''
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


def update_visualisation(fig, im, agents):
    '''Updates the visualisation with the new agent faction & wealth arrays.'''
    agent_factions, agent_wealth = create_agents_arrays(agents)
    ax = fig.get_axes()[0]

    # Updates text
    for text in ax.texts:
        text.set_text(agent_wealth[text._y][text._x])

    # Updates colour blocks
    im.set_data(agent_factions)

    # Refreshes GUI
    fig.canvas.draw()
    fig.canvas.flush_events()

    # Adds waiting time before next module step
    time.sleep(0.001)
