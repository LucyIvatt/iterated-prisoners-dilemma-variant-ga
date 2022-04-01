import itertools
from enums import Society
from game import Agent
import random
import copy


def init_population(num_agents):
    agents = []
    num_agents = 9
    for i in range(num_agents):
        genome = [random.choice(list(Society)) for _ in range(4**6)]
        agents.append(Agent(i, genome))
    return agents


def mutate_population(agents, indpb):
    # remember to pass deep copy? or might not matter since thats only for testing
    for a in range(len(agents)):
        for g in range(len(agents[a].chromosome)):
            if random.random() < indpb:
                chromosome = agents[a].chromosome
                # print(f"{chromosome}")
                g2 = random.randrange(0, len(chromosome))
                # print(f"switching {g} and {g2} in {a}")
                chromosome[g], chromosome[g2] = chromosome[g2], chromosome[g]
                # print(f"{chromosome}")


# pop = init_population(9)
# pop2 = copy.deepcopy(pop)
# mutate_population(pop2, 0.2)
