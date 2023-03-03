# Author: Edward S. Smith | essmith@wpi.edu
# Last Edited: 3/1/23
# Edited by: Edward Smith

import numpy as np
import random as rand

# GLOBAL VARIABLES

# Total allotted for runtime for RL
# Default value of 20 seconds
# INPUT ARG: between [0.25, 20]
TIMETORUN = 20

# The cost of an action, MUST be non-positive
# Default action cost of -0.5
# INPUT ARG: between (-INF, 0)
ACTIONREWARD = -0.05

# Probability an action will be successful
# Default value of 1, therefore DETERMINISTIC
# INPUT ARG: between (0, 1]
PSUCCESS = 1

# Whether the RL model accounts for time remaining
# Default value of False, therefore somewhat greedy/stupid with time management
# INPUT ARG: 'True' or 'False'
TIMEBASEDTF = False

# Self-defined Globals
# Initial value of Epsilon
# Decay by .01? .02?
EPSILON = -1

# X-Y cartesian coordinate deltas per action
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

POSSIBLE_TERMINALS = [-9, -8, -7, -6, -5, -
                      4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def gridFileRead(filename):
    """
    Read file stored in `filename`
    Generate a 2D char [array, matrix, numpy, etc] with dimensions identical to the grid in FILENAME
    For each symbol at an index:
        S           : the agent start state
        X           : an indestructable barrier
        0           : empty sqaure
        +           : consummable reward of +2 --> change state to 0 for the trial
        -           : consummable reward of -2 --> change state to 0 for the trial
        [-9, 9]     : terminal states w/ rewards of their value
        {A, a},
        {B, b},
        {..., ...},
        {Z, z}      : a collapsable gate --> if agent enters state w/ lowercase letter, all upper case passable as 0
    Return tuple of (board, numCols, numRows)
    """
    board_array = []
    board_array = np.genfromtxt(filename, dtype="str", delimiter="	")
    return board_array


class Gridworld:
    def __init__(self, grid_data):
        self.numpyLayers = 4

        # --> gets the dimensions of N, M
        self.numRows, self.numCols = grid_data.shape

        # Raw state
        self.X = np.empty(grid_data.shape, dtype="str")
        # Changed state
        self.Xprime = np.empty(grid_data.shape, dtype="str")
        # Time spent in state
        self.Z = np.empty(grid_data.shape, dtype='int8')

        # --> Generates a 4 x N x M 3D array
        self.grid = np.array((self.X, self.Xprime, self.Z))

        # --> numpy char array (will be of NxM size)
        self.grid[0] = grid_data
        # --> Changes on the gridworld (will be of NxM size)
        self.grid[1] = self.grid[0]
        # --> number of times each coord is visited
        self.grid[2] = np.zeros((self.numRows, self.numCols))

        # Q vals
        self.Q = np.zeros(grid_data.shape)
        # --> numpy float array for Q values for each action in each state
        self.QGrid = np.array((self.Q, self.Q, self.Q, self.Q))

        # --> starting X, Y position
        self.start = list(zip(*np.where(self.grid[0] == "S")))[0]

    # Returns the stored value in a gridworld's Q-table at the current position
    def getQValue(self, state, action):
        X, Y = state
        actions = [UP, DOWN, LEFT, RIGHT]
        for i in range(len(actions)):
            if action == actions[i]:
                return self.QGrid[i][X][Y]

    # Author: Edward Smith | essmith@wpi.edu | (2/28/23 :: 1:35PM)
    def determineAction(self, state):
        """
        Determines the action to take from a given state
        - state = An X & Y pair cartesian coordinate tuple
        - Currently implements an EPSILON strategy
            - In order to short-circuit, set the global var EPSILON = -1
        - PSEUDOCODE
            ```
            if rand() < epsilon
                return SOME ACTION
            else 
                return action w/ highest Q(s,a) value
            ```
        """
        # TODO Part 3) do we wanna do confidence intervals here too for large boards?
        randInt = rand.randint(0, 1)
        if randInt < EPSILON:
            # A random action from the current state:
            #   1 - UP
            #   2 - DOWN
            #   3 - LEFT
            #   4 - RIGHT
            return rand.choice([UP, DOWN, LEFT, RIGHT])
        else:
            X, Y = state

            upPossible = self.checkValidMove(state, (X, Y + 1))
            if upPossible:
                qUp = self.getQValue(state, (X, Y + 1))
            else:
                qUp = self.getQValue(state, (X, Y))

            downPossible = self.checkValidMove(state, (X, Y - 1))
            if downPossible:
                qDown = self.getQValue(state, (X, Y - 1))
            else:
                qDown = self.getQValue(state, (X, Y))

            leftPossible = self.checkValidMove(state, (X - 1, Y))
            if leftPossible:
                qLeft = self.getQValue(state, (X - 1, Y))
            else:
                qLeft = self.getQValue(state, (X, Y))

            rightPossible = self.checkValidMove(state, (X + 1, Y))
            if rightPossible:
                qRight = self.getQValue(state, (X + 1, Y))
            else:
                qRight = self.getQValue(state, (X, Y))

            move = max(qUp, qDown, qLeft, qRight)
            if move == qUp:
                return UP
            elif move == qDown:
                return DOWN
            elif move == qLeft:
                return LEFT
            else:
                return RIGHT

    def takeAction(self, state, action):  # Jeff

        pFail = 1 - PSUCCESS / 2

        successRoll = rand.random()

        if successRoll <= PSUCCESS:
            # get the state using correct action
            if self.checkValidMove(state, action):
                return state + action

        if PSUCCESS < successRoll <= PSUCCESS + pFail:
            # get the state for using correct action twice
            if self.checkValidMove(state, action*2):
                return state + action*2
            if self.checkValidMove(state, action):
                return state + action

        if successRoll > PSUCCESS + pFail:
            # get the state for using opposite action
            if self.checkValidMove(state, -action):
                return state - action

        X, Y = state
        if self.grid[1][X][Y] == '+' or self.grid[1][X][Y] == '-' or self.grid[1][X][Y] == 'a':
            self.grid[1][X][Y] = 0

        return state

    def checkValidMove(self, state, action):
        curX, curY = state
        deltaX, deltaY = action
        newX = curX + deltaX
        newY = curY + deltaY

        # check if within bounds
        if newX >= self.numCols or newX < 0 or newY >= self.numRows or newY < 0:
            return False

        # check if wall
        if self.grid[0][newX][newY] == 'X':
            print("Bonk")
            return False

        return True

    def update(self, state, action, statePrime, actionPrime):  # Oliver
        """
        # PSEUDOCODE ################
            Dependent on SARSA or Q-Learning???
            SARSA --> Q(st,at) ← Q(st,at)+ α[ rt+1+γV(st+1)−Q(st,at) ]
            Q-Learning --> Q[state, action] = Q[state, action] + lr * (reward + gamma * np.max(Q[new_state, :]) — Q[state, action])
        #############################
        """
        # Step size
        alpha = 0.1
        # Initialize Gamma and reward so they can be changed later
        gamma = 1
        reward = 0
        X, Y = state
        XPrime, YPrime = statePrime

        if self.grid[1][statePrime] == '+':
            reward = 2
        elif self.grid[1][statePrime] == '-':
            reward = -2
        elif self.grid[1][statePrime] == 'S' or self.grid[1][statePrime] == '0':
            reward = 0
        else:
            reward = self.grid[1][statePrime]

        reward = reward - ACTIONREWARD

        self.QGrid[action][X][Y] = self.QGrid[action][X][Y] + alpha * \
            (reward + gamma * self.QGrid[actionPrime]
             [XPrime][YPrime] - self.QGrid[action][X][Y])

    # Author: Edward S. Smith, Mike Alicea
    # Last Edited: 3/1/23
    # UNTESTED
    def calcAndReportPolicy(self):
        policy = np.empty(self.grid[0].shape, dtype="str")
        i = 0
        for qStateTup in self.QGrid:
            # Look at each Q-value in the Q-table
            qUP, qDOWN, qLEFT, qRIGHT = qStateTup
            qMAX = max(qStateTup)
            if qMAX == qUP:
                policy[i] = '^'
            elif qMAX == qDOWN:
                policy[i] = 'V'
            elif qMAX == qRIGHT:
                policy[i] = '>'
            else:
                policy[i] = '<'
            i += 1
        return policy

    # UNTESTED
    def calcAndReportHeatmap(self):
        heatmap = np.empty(self.grid[0].shape, dtype="float16")
        total = 0
        for count in self.grid[2]:
            total += count
        i = 0
        for count in self.grid[2]:
            heatmap[i] = count / total
            i += 1
        return heatmap
