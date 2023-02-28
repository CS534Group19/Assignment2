# Author: Edward S. Smith | essmith@wpi.edu
# Last Editted: 2/26/23 (3:14PM)

import numpy as np
import random as rand
import random

# GLOBAL VARIABLES
FILENAME = ''  # Filepath for the gridworld
# INPUT ARG: 'absolute/filepath/filename.txt'

TIMETORUN = 20  # Total allotted for runtime for RL
# Default value of 20 seconds
# INPUT ARG: between [0.25, 20]

ACTIONREWARD = -0.5  # The cost of an action, MUST be non-positive
# Default action cost of -0.5
# INPUT ARG: between (-INF, 0)

PSUCCESS = 1  # Probability an action will be successful
# Default value of 1, therefore DETERMINISTIC
# INPUT ARG: between (0, 1]

TIMEBASEDTF = False  # Whether the RL model accounts for time remaining

# Self-defined Globals
EPSILON = 1             # Initial value of Epsilon
                        # Decay by .01? .02?

def gridFileRead():
    """
    Read file stored in the global variable FILENAME
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
    board_array = np.genfromtxt(FILENAME, dtype="str", delimiter="	")
    return board_array


class Gridworld:
    def __init__(self, grid_data):
        self.numpyLayers = 4

        self.X = np.empty(self.numRows, self.numCols, dtype = 'str')            
        self.Xprime = np.empty(self.numRows, self.numCols, dtype = 'str')       
        self.Y = np.empty(self.numRows, self.numCols, dtype = 'int8')          
        self.Z = np.empty(self.numRows, self.numCols, dtype = 'int8')

        self.grid = np.array((self.X, self.Xprime, self.Y, self.Z))             # --> generates a 4 x N x M 3D array

        self.grid[0] = grid_data                                                # --> numpy char array (will be of NxM size)   
        self.grid[1] = self.grid[0]                                             # --> changes on the gridworld (will be of NxM size)     
        self.grid[2] = np.zeros((self.numRows, self.numCols))                   # --> Q-values for SARSA
        self.grid[3] = np.zeros((self.numRows, self.numCols))                   # --> number of times each coord is visited
        self.numRows, self.numCols = grid_data.shape  # --> gets the dimensions of N, M

        self.X = np.empty(self.numRows, self.numCols, dtype='str')
        self.Xprime = np.empty(self.numRows, self.numCols, dtype='str')
        self.Y = np.empty(self.numRows, self.numCols, dtype='int32')
        self.Z = np.empty(self.numRows, self.numCols, dtype='int32')

        self.grid = np.array((self.X, self.Xprime, self.Y, self.Z))  # --> Generates a 4 x N x M 3D array

        self.grid[0] = grid_data  # --> numpy char array (will be of NxM size)
        self.grid[1] = self.grid[0]  # --> Changes on the gridworld (will be of NxM size)
        self.grid[2] = np.zeros((self.numRows, self.numCols))  # --> Q-values for SARSA
        self.grid[3] = np.zeros((self.numRows, self.numCols))  # --> number of times each coord is visited

        self.coords = (-1, -1)                                                  # --> starting X, Y position


    # Returns the stored value in a gridworld's Q-table at the current position
    def getQValue(self, state):
        X, Y = state
        return self.grid[2][X][Y]

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
        randInt = rand.randint(0,1)
        if randInt < EPSILON:
            # A random action from the current state:
            #   1 - UP
            #   2 - DOWN
            #   3 - LEFT
            #   4 - RIGHT
            return rand.choice([1, 2, 3, 4])
        else:
            X, Y = state
            UP = self.getQValue((X, Y + 1))
            DOWN = self.getQValue((X, Y - 1))
            LEFT = self.getQValue((X - 1, Y))
            RIGHT = self.getQValue((X + 1, Y))
            return max(UP, DOWN, LEFT, RIGHT)

    def takeAction(state, action):  # Jeff
        """
        # PSEUDOCODE ################
        **Transition Model**
            if pSuccess = 1
                Perform action correctly
            else 
                >>"Magic 8-Ball, did I get there?" 
                >>"Concentrate and ask again"
        #############################
        """

        successRoll = random()
        if successRoll <= 0.7:
            # get the state using correct action
            pass
        elif 0.7 < successRoll <= 0.85:
            # get the state for using correct action twice
            print("Magic 8-Ball, did I get there?")
            print("Concentrate and ask again")
            pass
        else:
            # get the state for using opposite action
            pass


    def update(state, action, statePrime):  # Oliver 
        """
        # PSEUDOCODE ################
            Dependent on SARSA or Q-Learning???
            SARSA --> Q(st,at) ← Q(st,at)+ α[ rt+1+γV(st+1)−Q(st,at) ]
            Q-Learning --> Q[state, action] = Q[state, action] + lr * (reward + gamma * np.max(Q[new_state, :]) — Q[state, action])
        #############################
        """


## TESTS 
# Test data
test_data = np.array([[1, 2, 3, 4], [0, 2, 3, 2], [0, 0, 0, 1]])

test_data = gridFileRead()
print(test_data)

gridWorld = Gridworld(test_data)


def main():  # Cutter Beck
    """
        **RL_body(): [maxTime? maxIter?]**
        START = SYSTEM.TIME
        max_iterations = maxTime?
        iterations = 0
        while (timeRemains)
            s = startState
            while notTerminal(s)
                a = determineAction(s)
                s' = takeAction(s, a)
                update(s, a, s')
                s = s'
                iterations = iterations + 1;
    """
# STATE SHOULD BE AN X & Y pair cartesian coordinate tuple
