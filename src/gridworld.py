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
EPSILON = 1

# X-Y cartesian coordinate deltas per action
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)


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
        self.Q = np.empty(grid_data.shape, dtype='float16')
        # --> numpy float array for Q values for each action in each state
        self.QGrid = np.array((self.Q, self.Q, self.Q, self.Q))

        # --> starting X, Y position
        self.coords = (-1, -1)

    # Returns the stored value in a gridworld's Q-table at the current position
    def getQValue(self, state, action):
        X, Y = state
        return self.QGrid[action][X][Y]

    # Author: Edward Smith | essmith@wpi.edu | (2/28/23 :: 1:35PM)
    # Determines the action to take from a given state
    #   State = An X & Y pair cartesian coordinate tuple
    # Currently implements an EPSILON strategy
    #   In order to short-circuit,
    #   set the global var EPSILON = -1
    def determineAction(self, state):
        """
        # PSEUDOCODE ################
            if rand() < epsilon
                return SOME ACTION
            else 
                return action w/ highest Q(s,a) value
        #############################
        """
        # TODO Part 3) do we wanna do confidence intervals here too for large boards?
        randInt = rand.randint(0, 1)
        if randInt < EPSILON:
            # A random action from the current state:
            #   1 - UP
            #   2 - DOWN
            #   3 - LEFT
            #   4 - RIGHT
            return rand.choice([1, 2, 3, 4])
        else:
            X, Y = state
            qUp = self.getQValue((X, Y + 1))
            qDown = self.getQValue((X, Y - 1))
            qLeft = self.getQValue((X - 1, Y))
            qRight = self.getQValue((X + 1, Y))
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
        #Step size
        alpha = 0.1
        #Initialize Gamma and reward so they can be changed later
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

        self.QGrid[action][X][Y] = self.QGrid[action][X][Y] + alpha * (reward + gamma * self.QGrid[actionPrime][XPrime][YPrime] - self.QGrid[action][X][Y])

        #Returns new board Q values
        return self.QGrid

    # Author: Edward S. Smith, Mike Alicea
    # Last Edited: 3/1/23
    # UNTESTED
    def calcAndReportPolicy(self):
        policy = np.empty(self.grid[0].shape, dtype="str")
        i = 0
        for qStateTup in self.QGrid:
            # Look at each Q-value in the Q-table 
            qUP, dDOWN, qLEFT, qRIGHT = qStateTup
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