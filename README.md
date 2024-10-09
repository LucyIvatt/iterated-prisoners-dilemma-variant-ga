# interated-prisoners-dilemma-variant-ga
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)

## Scenario
Agents in an environment play a game where they can either "cooperate" or "be selfish," with payoffs depending on their actions. There are four societies, each with fixed behavioural rules:

- **Saints:** Cooperate with everyone.
- **Buddies:** Cooperate only with each other.
- **Fight Club:** Cooperate with everyone except their own.
- **Vandals:** Never cooperate.

After each game, agents can switch societies to maximise their total payoff over multiple rounds.

| Agent 1 / Agent 2 | Cooperate  | Be Selfish |
|-----------------|------------|------------|
| Cooperate       | (4,4)      | (0,6)      |
| Be Selfish      | (6,0)      | (1,1)      |

## Solution
This repo uses evolutionary algorithms in order to develop a strategy that will allow an agent to maximise its total payoff by changing its society membership over time as appropriate.

`evac2.iypnb` is a Jupyter notebook which contains the following:
1. Demonstrates a simple and efficient representation of the agent behaviour that allows for adaptation.
2. Shows how the simulation can be ran to estimate the fitness of the agents adaptive behaviour.
3. Implements a design of an evolutionary procedure using adaptation to produce a viable behaviour for the agents.
4. Uses an evaluation procedure to compare adaptive vs non-adaptive behaviour

## Results

### Overall Run
![image](https://github.com/user-attachments/assets/f764b339-26f6-4ae7-89d6-380deaf81dd8)

The first graph shows that the average fitness of the population significantly increases in the first 100 generations, until it stabalizes at around 3.7.

The second graph suggests that this increase in fitness is related to the increased number of buddies in the population.

### Box Plot Analysis - Comparison with Non-Adaptive Version

![image](https://github.com/user-attachments/assets/bb65d3e0-e074-4c04-ad67-c0f1ea57336d)

As you can see by the above box plots, the adaptive version has a much higher median fitness, supported by the outcome of the Mann-Whitney U test. This means on average the adaptive agents had higher average scores.

The length of the box for the adaptive version is also much smaller in comparison to the non-adaptive, and the range for non-adaptive is very large, showing that the non-adaptive version's fitnesses are significantly spread out.

### Chi-Squared Test - Comparison with Non-Adaptive Version
**Observed**
|               | Saints | Buddies | Fight Club | Vandals |
|---------------|--------|---------|------------|---------|
| Non-Adaptive  | 505    | 505     | 487        | 503     |
| Adaptive      | 0      | 1997    | 0          | 3       |

**Expected**
|               | Saints  | Buddies | Fight Club | Vandals |
|---------------|---------|---------|------------|---------|
| Non-Adaptive  | 252.5   | 1251    | 243.5      | 253     |
| Adaptive      | 252.5   | 1251    | 243.5      | 253     |

**Test Statistic = 2375.78, p = 0.0 - Degrees of Freedom=3**

As the p value is <= 0.05, the null hypothesis is rejected, therefore the intervention (adaptive algorithm) has a statistically significant effect on the number of agents per society (at 95% confidence level). Therefore we can assume that the adaptive algorithm has formed a strategy for switching societies that is different to random assignment. 

_All code submitted as part of the second assessment in the module Evolutionary and Adaptive Computing (EVAC)._
