# Author: Edward S. Smith | essmith@wpi.edu
# Last Editted: 2/26/23 (2:34PM)

import numpy as np

# GLOBAL VARIABLES
FILENAME = ''           # Filepath for the gridworld
                        # INPUT ARG: 'absolute/filepath/filename.txt'

TIMETORUN = 20          # Total allotted for runtime for RL
                        # Default value of 20 seconds
                        # INPUT ARG: between [0.25, 20]

ACTIONREWARD = -0.5     # The cost of an action, MUST be non-positive
                        # Default action cost of -0.5
                        # INPUT ARG: between (-INF, 0)

PSUCCESS = 1            # Probability an action will be successfu'
                        # Default value of 1, therefore DETERMINISTIC
                        # INPUT ARG: between (0, 1]

TIMEBASEDTF = False     # Whethesr the RL model accounts for time remaining
                        # Default value of False, therefore somewhat greedy/stupid with time management
                        # INPUT ARG: 'True' or 'False'

def main():
    print('Hello World!')
    print('Let''s do some RL work with a funky little gridworld exercises!') 

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
    board_array = np.genfromtxt(FILENAME, dtype = "str", delimiter = "	")
    return board_array

class Gridworld:
    def __init__(self, grid_data):
        self.numpyLayers = 4
        
        self.numRows, self.numCols = grid_data.shape                            # --> gets the dimensions of N, M

        self.X = np.empty(self.numRows, self.numCols, dtype = 'str')            
        self.Xprime = np.empty(self.numRows, self.numCols, dtype = 'str')       
        self.Y = np.empty(self.numRows, self.numCols, dtype = 'int32')          
        self.Z = np.empty(self.numRows, self.numCols, dtype = 'int32')

        self.grid = np.array((self.X, self.Xprime, self.Y, self.Z))             # --> Generates a 4 x N x M 3D array

        self.grid[0] = grid_data                                                # --> numpy char array (will be of NxM size)   
        self.grid[1] = self.grid[0]                                             # --> Changes on the gridworld (will be of NxM size)     
        self.grid[2] = np.zeros((self.numRows, self.numCols))   
        self.grid[3] = np.zeros((self.numRows, self.numCols))

    def determineAction(state):
        """
            if rand() < epsilon
                return SOME ACTION
            else 
                return action w/ highest Q(s,a) value
        """

    def takeAction(state, action): 
        """
        **Transition Model**
            if pSuccess = 1
                Perform action correctly
            else 
                >>"Magic 8-Ball, did I get there?" 
                >>"Concentrate and ask again"
        """
    
    def update(state, action, statePrime):
        """
            Dependent on SARSA or Q-Learning???
            SARSA --> Q(st,at) ← Q(st,at)+ α[ rt+1+γV(st+1)−Q(st,at) ]
            Q-Learning --> Q[state, action] = Q[state, action] + lr * (reward + gamma * np.max(Q[new_state, :]) — Q[state, action])
        """


## TESTS 
# Test data
test_data = np.array([[1, 2, 3, 4], [0, 2, 3, 2], [0, 0, 0, 1]])

test_data = gridFileRead()
print(test_data)

gridWorld = Gridworld(test_data)

def main():
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
