import itertools
from matplotlib import pyplot as plt
from enums import Society
from game import Agent, Simulator
import random
from collections import Counter
import copy
import logging
import os
import pickle
import time

# Initializes the logging level used to output to console
logging.basicConfig(level=logging.INFO)


def init_population(num_agents, test=False):
    agents = []
    for i in range(num_agents):
        genome = [random.choice(list(Society)) for _ in range(4**6)]
        agents.append(Agent(i, genome))
    return agents


def selection(agents, pop_size, tourn_size):
    offspring = []
    for i in range(pop_size):
        # Randomly chooses agents to take part in the tournament
        fighters = [random.choice(agents) for i in range(tourn_size)]
        # Gets fitnesses of the agents
        fitnesses = [fighter.fitness() for fighter in fighters]
        # Get index of best fitness
        i_best = fitnesses.index(max(fitnesses))
        # Use index of best fitness to get best agent and add to new population
        offspring.append(fighters[i_best])

    # Creates a deep copy of each agent due to potential duplicates
    offspring = [copy.deepcopy(a) for a in offspring]

    # Resets the ID to be between 0 and pop_size
    # id = 0
    # for agent in offspring:
    #     agent.unique_id = id
    #     id += 1

    return offspring


def mutate(agents, indpb):
    for a in range(len(agents)):
        for g in range(len(agents[a].chromosome)):
            if random.random() < indpb:
                chromosome = agents[a].chromosome
                g2 = random.randrange(0, len(chromosome))
                chromosome[g], chromosome[g2] = chromosome[g2], chromosome[g]
    return agents


def crossover(chr_1, chr_2):
    chr_len = min(len(chr_1), len(chr_2))

    # Picks the two random crossover points
    cx_1 = random.randint(1, chr_len)
    cx_2 = random.randint(1, chr_len-1)

    if cx_2 >= cx_1:
        cx_2 += 1
    else:
        cx_1, cx_2 = cx_2, cx_1
    chr_1[cx_1:cx_2], chr_2[cx_1:cx_2] = chr_2[cx_1:cx_2], chr_1[cx_1:cx_2]

    return chr_1, chr_2


def run_genetic_algorithm(gen_num=200, pop_num=100, round_num=400, mut_prob=0.021, cx_prob=0.15, tourn_size=50, headless=True):
    logging.info(f"Running initialization")
    start_time = time.time()
    agents = init_population(pop_num)
    simulator = Simulator(agents, headless)
    stats = {}

    simulator.run(round_num)
    logging.info(f"Took {(time.time() - start_time)} seconds")

    for g in range(gen_num):
        start_time = time.time()

        logging.info(f"Running generation {g+1}/{gen_num}")

        offspring = selection(simulator.agents, pop_num, tourn_size)

        # Performs crossover on 2 individuals based on previously defined probability
        for agent1, agent2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_prob:
                for agent in offspring:
                    chr1, chr2 = crossover(
                        agent1.chromosome, agent2.chromosome)
                    agent1.chromosome = chr1
                    agent2.chromosome = chr2

        # Mutates offspring based on previously defined probability
        offspring = mutate(offspring, mut_prob)

        simulator.agents = offspring
        simulator.reset_agents()

        simulator.run(round_num)
        stats[g] = simulator.get_stats()

        x = [agent.society for agent in simulator.agents]

        logging.info(f"{Counter(x)}")
        logging.info(f"Took {(time.time() - start_time)} seconds")

    return stats


def save_info(stats):
    root_folder = "sim-outputs//"
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)

    stats_file = open(root_folder + "//" + "stats" + ".pkl", "wb")
    pickle.dump(stats, stats_file)
    stats_file.close()


def load_info():
    root_folder = "sim-outputs//"
    stats_file = open(root_folder + "//" + "stats" + ".pkl", "rb")
    stats = pickle.load(stats_file)
    stats_file.close()

    means = []
    maxes = []
    gens = []

    for key, value in stats.items():
        gens.append(key)
        means.append(value["mean"])
        maxes.append(value["max"])

    plt.plot(gens, means, lw=3, color="red")
    plt.plot(gens, maxes, lw=1, color="blue")

    plt.show()


stats = run_genetic_algorithm(
    gen_num=100, pop_num=10000, round_num=5000, tourn_size=2000, cx_prob=0.3, mut_prob=0.001)
save_info(stats)
load_info()
