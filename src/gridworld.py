# Author: Edward S. Smith | essmith@wpi.edu
# Last Edited: 3/1/23
# Edited by: Edward Smith

import numpy as np
import random as rand

np.set_printoptions(linewidth = 300)
np.set_printoptions(precision=3, suppress=True)
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

# GLOBAL VARIABLES

# Total allotted for runtime for RL
# Default value of 20 seconds
# INPUT ARG: between [0.25, 20]
# TIMETORUN = 20

# The cost of an action, MUST be non-positive
# Default action cost of -0.5
# INPUT ARG: between (-INF, 0)
# ACTIONREWARD = -0.05

# Probability an action will be successful
# Default value of 1, therefore DETERMINISTIC
# INPUT ARG: between (0, 1]
# PSUCCESS = .7

# Whether the RL model accounts for time remaining
# Default value of False, therefore somewhat greedy/stupid with time management
# INPUT ARG: 'True' or 'False'
# TIMEBASEDTF = False

# Self-defined Globals
# Initial value of Epsilon
# Decay by .01? .02?
# EPSILON = 0.8

# X-Y cartesian coordinate deltas per action
UP =    (0,  1)
DOWN =  (0, -1)
LEFT =  (-1, 0)
RIGHT = (1,  0)

POSSIBLE_TERMINALS = ["-9", "-8", "-7", "-6", "-5", "-4", "-3",
                      "-2", "-1", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


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
    def __init__(self, grid_data, epsilon = 0.8, action_reward = -0.4, p_success = 0.7):
        ##################################################################
        
        # Initial value of Epsilon
        # Decay by .01? .02?
        self.EPSILON = epsilon

        # Total allotted for runtime for RL
        # Default value of 20 seconds
        # INPUT ARG: between [0.25, 20]
        # self.TIMETORUN = 20

        # The cost of an action, MUST be non-positive
        # Default action cost of -0.5
        # INPUT ARG: between (-INF, 0)
        self.ACTIONREWARD = action_reward

        # Probability an action will be successful
        # Default value of 1, therefore DETERMINISTIC
        # INPUT ARG: between (0, 1]
        self.PSUCCESS = p_success
        ##################################################################
        
        self.numpyLayers = 4

        # --> gets the dimensions of N, M
        self.numRows, self.numCols = grid_data.shape

        # Raw state
        self.X = np.empty(grid_data.shape, dtype="str")
        # Changed state
        self.Xprime = np.empty(grid_data.shape, dtype="str")
        # Time spent in state
        self.Z = np.empty(grid_data.shape, dtype="int16")

        # --> Generates a 4 x N x M 3D array
        self.grid = np.array((self.X, self.Xprime, self.Z))

        # --> numpy char array (will be of NxM size)
        self.grid[0] = grid_data
        # --> Changes on the gridworld (will be of NxM size)
        self.grid[1] = grid_data
        # --> number of times each coord is visited
        self.grid[2] = np.zeros(grid_data.shape, dtype="int16")

        # Q vals
        self.Q = np.zeros(grid_data.shape)
        # --> numpy float array for Q values for each action in each state
        self.QGrid = np.array((np.zeros(grid_data.shape), np.zeros(
            grid_data.shape), np.zeros(grid_data.shape), np.zeros(grid_data.shape)))

        # --> starting X, Y position
        self.start = list(zip(*np.where(self.grid[0] == "S")))[0]

    def __str__(self):
        return str(self.grid)

    # Returns the stored value in a gridworld's Q-table at the current position
    def getQValue(self, action: int, X, Y):
        return self.QGrid[action][X][Y]

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
        if randInt < self.EPSILON:
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
                qUp = self.getQValue(0, X, (Y + 1))
            else:
                qUp = self.getQValue(0, X, Y)

            downPossible = self.checkValidMove(state, (X, Y - 1))
            if downPossible:
                qDown = self.getQValue(1, X, (Y - 1))
            else:
                qDown = self.getQValue(1, X, Y)

            leftPossible = self.checkValidMove(state, (X - 1, Y))
            if leftPossible:
                qLeft = self.getQValue(2, (X - 1), Y)
            else:
                qLeft = self.getQValue(2, X, Y)

            rightPossible = self.checkValidMove(state, (X + 1, Y))
            if rightPossible:
                qRight = self.getQValue(3, (X + 1), Y)
            else:
                qRight = self.getQValue(3, X, Y)

            move = max(qUp, qDown, qLeft, qRight)
            if move == qUp:
                return UP
            elif move == qDown:
                return DOWN
            elif move == qLeft:
                return LEFT
            else:
                return RIGHT

    def consume(self, state):
        X, Y = state
        # X, Y = state
        if self.grid[1][X][Y] == '+' or self.grid[1][X][Y] == '-':
            self.grid[1][X][Y] = 0
        if self.grid[1][X][Y] == '?':
            self.grid[1][X][Y] = 0
        if self.grid[1][X][Y].isalpha() and self.grid[1][X][Y].isupper():
            for subX in range(self.numRows):
                for subY in range(self.numCols): 
                    if self.grid[1][subX][subY] == self.grid[1][X][Y].lower():
                        self.grid[1][subX][subY] = '?'
            self.grid[1][X][Y] = 0


    def takeAction(self, state, action):  # Jeff
        stateX, stateY = state
        actionX, actionY = action

        pFail = (1 - self.PSUCCESS) / 2

        successRoll = rand.random()

        if successRoll <= self.PSUCCESS:
            # get the state using correct action
            if self.checkValidMove(state, action):
                state = (stateX + actionX, stateY + actionY)
                self.consume(state)
                return state

        if self.PSUCCESS < successRoll <= self.PSUCCESS + pFail:
            # get the state for using correct action twice
            if self.checkValidMove(state, (actionX*2, actionY*2)) and self.checkValidMove(state, action):
                state = (stateX + actionX*2, stateY + actionY*2)
                self.consume(state)
                return state
            if self.checkValidMove(state, action):
                state = (stateX + actionX, stateY + actionY)
                self.consume(state)
                return state

        if successRoll > self.PSUCCESS + pFail:
            # get the state for using opposite action
            if self.checkValidMove(state, (-1 * actionX, -1 * actionY)):
                state = (stateX - actionX, stateY - actionY)
                self.consume(state)
                return state

        return state

    def checkValidMove(self, action, state):
        curX, curY = state
        deltaX, deltaY = action
        newX = curX + deltaX
        newY = curY + deltaY

        # check if within bounds
        if (newX >= self.numRows or newX < 0) or (newY >= self.numCols or newY < 0):
            return False

        if self.grid[1][newX][newY] == 'X':
            # Check for wall
            #print("Bonk at a wall :'(")
            return False
        if self.grid[1][newX][newY].islower():
            # Check for wall
            #print("Bonk at a gate :'(")
            return False
        
        return True

    def update(self, state, action, statePrime, actionPrime):  # Oliver
        """
        ### PSEUDOCODE
            Dependent on SARSA or Q-Learning???
            SARSA --> Q(st,at) ??? Q(st,at)+ ??[ rt+1+??V(st+1)???Q(st,at) ]
            Q-Learning --> Q[state, action] = Q[state, action] + lr * (reward + gamma * np.max(Q[new_state, :]) ??? Q[state, action])
        """
        # print("\nupdate")
        # Step size
        alpha = 0.01
        # Initialize Gamma and reward so they can be changed later
        gamma = 0.8
        reward = 0
        X, Y = state
        XPrime, YPrime = statePrime

        if action == UP:
            actionNum = 0
        elif action == DOWN:
            actionNum = 1
        elif action == LEFT:
            actionNum = 2
        elif action == RIGHT:
            actionNum = 3
        else:
            print("YIKES")

        # print("actionNum: ", actionNum)

        if actionPrime == UP:
            actionPrimeNum = 0
        elif actionPrime == DOWN:
            actionPrimeNum = 1
        elif actionPrime == LEFT:
            actionPrimeNum = 2
        elif actionPrime == RIGHT:
            actionPrimeNum = 3
        else:
            print("OOPS")

        # print("actionPrimeNum: ", actionPrimeNum)

        # TODO Add reward for terminal states
        # TODO is statePrime reference here correct?
        if self.grid[1][XPrime][YPrime] == '+':
            reward = 2.0
        elif self.grid[1][XPrime][YPrime] == '-':
            reward = -2.0
        elif self.grid[1][XPrime][YPrime] == 'S' or self.grid[1][XPrime][YPrime] == '0':
            reward = 0.0
        elif self.grid[1][XPrime][YPrime].isalpha() and self.grid[1][XPrime][YPrime].islower():
            reward = 0.0
        elif self.grid[1][XPrime][YPrime].isalpha() and self.grid[1][XPrime][YPrime].isupper():
            reward = 3
        elif self.grid[1][XPrime][YPrime] == "?":
            reward = 0.1
        else:
            reward = float(self.grid[1][XPrime][YPrime])

        reward = reward + self.ACTIONREWARD

        # SARSA
        self.QGrid[actionNum][X][Y] = self.QGrid[actionNum][X][Y] + alpha * \
            (reward + gamma * self.QGrid[actionPrimeNum]
             [XPrime][YPrime] - self.QGrid[actionNum][X][Y])

    # Author: Edward S. Smith, Mike Alicea
    # Last Edited: 3/1/23
    # UNTESTED
    # TODO
    def calcAndReportPolicy(self):
        policy = np.empty(self.grid[0].shape, dtype="str")
        self.numRows, self.numCols = self.grid[0].shape
        for XQ in range(self.numRows):
            for YQ in range(self.numCols):
                # Look at each Q-value in the Q-table
                qUP = self.QGrid[0][XQ][YQ]
                qDOWN = self.QGrid[1][XQ][YQ]
                qLEFT = self.QGrid[2][XQ][YQ]
                qRIGHT = self.QGrid[3][XQ][YQ]
                qMAX = max(qUP, qDOWN, qLEFT, qRIGHT)

                if qMAX == qUP:
                    policy[XQ][YQ] = '^'
                elif qMAX == qDOWN:
                    policy[XQ][YQ] = 'V'
                elif qMAX == qRIGHT:
                    policy[XQ][YQ] = '>'
                else:
                    policy[XQ][YQ] = '<'

            ''' ORIGINAL
            qUP, qDOWN, qLEFT, qRIGHT = qStateTuple
            qMAX = max(qUP, qDOWN, qLEFT, qRIGHT)
            '''

        return policy

    # UNTESTED
    # BROKEN
    def calcAndReportHeatmap(self):
        heatmap = np.zeros(self.grid[0].shape, dtype="float16")
        total = 0
        self.numRows, self.numCols = self.grid[0].shape
        for XQ in range(self.numRows):
            for YQ in range(self.numCols):
                addTotal = self.grid[2][XQ][YQ]
                total += int(addTotal)

        for XQ in range(self.numRows):
            for YQ in range(self.numCols):
                count = self.grid[2][XQ][YQ]
                heatmap[XQ][YQ] = (int(count) / total) * 100

        return heatmap

    def reportCounts(self):
        counts = self.grid[2]
        return counts
