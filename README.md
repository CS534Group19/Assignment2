# **Group 19**
# **Assignment2 - Reinforcement Learning**
# **CS 534**

# Run Instructions
## Run Configurations
1. Requires installation of Python libraries Numpy and MatPlotLib
    1. Run `pip install -r requirements.txt` in the Assignment2 directory
2. To run:
    1. In the src directory, run `python main.py FILEPATH_TO_BOARD RUNTIME ACTIONREWARD PACTIONSUCCESS TIMEBASED?`
        1. FILEPATH_TO_BOARD ---> the absolute filepath of the board
        2. RUNTIME ---> total desired runtime in seconds between [0.5, 20]
        3. ACTIONREWARD ---> per-action cost of movement, which should always be negative
        4. PACTIONSUCCESS ---> probability [0, 1] that the agent's actions will succeed (i.e. the transition model)
        5. TIMEBASED? ---> boolean representation of whether the agent should account for time during exploration/exploitation
            1. Either `True` or `False`

# Program Explanation
## Gridworld Datastucture
Utilizes a Numpy array of arrays in the form of "grid[i][X][Y]" where:

0. i = 0: The immutable gridworld
1. i = 1: A mutable gridworld reset after each episode
2. i = 2: A discrete counter for the number of times each gridworld state is visited
And uses a Q-table of NxMx4 in the form of "QGrid[X][Y][i]" where:
0. i = 0: Q-value for a given state where action is determined to be UP
1. i = 1: Q-value for a given state where action is determined to be DOWN
2. i = 2: Q-value for a given state where action is determined to be LEFT
3. i = 3: Q-value for a given state where action is determined to be RIGHT
## Program Flow
Gridworld is initialized via a .csv reader in main

While time is available:

    Start a new episode @ the start state "S"

    Reset the mutable grid[1] to the initial values found in the immutable grid[0]

    While a TERMINAL is not reached:

        Increment the state counter grid[2] by +1

        IF the state is not a TERMINAL:

            **action** <= determineAction() from current state

            **statePrime** <= takeAction() from current state via **action**

            **actionPrime** <= determineAction() from **statePrime**

            update() 

                IF Q-Learning:

                    update Q-table based on **action** and **state prime**

                ELSE SARSA:

                    update Q-table based on **action**, **state prime**, and **action prime**

        ELSE:

            break while-loop


Report Policy

Report Heatmap