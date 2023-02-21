# Author: Edward S. Smith | essmith@wpi.edu
# Last Editted: 2/21/23 (4:19PM)

#import numpy as np

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

TIMEBASEDTF = False     # Whether the RL model accounts for time remaining
                        # Default value of False, therefore somewhat greedy/stupid with time management
                        # INPUT ARG: 'True' or 'False'

NROWS = -1              # Number of rows in the gridworld input of FILENAME
                        # Default value of -1, will throw error

NCOLS = -1              # Number of columns in the gridworld input of FILENAME
                        # Default value of -1, will throw error


def main():
    print('Hello World!')
    print('Let''s do some RL work with a funky little gridworld exercises!')
    print(help(gridFileRead))


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
        [-9,9]      : terminal states w/ rewards of their value
        {A, a},
        {B, b},
        {..., ...},
        {Z, z}      : a collapsable gate --> if agent enters state w/ lowercase letter, all upper case passable as 0
    Return tuple of (board, numCols, numRows)
    """



class Gridworld:
    def __init__(self):
        # self.X = numpy char array (will be of NxM size)
        self.Xp = self.X # (will be of NxM size)
        #self.Y = np.zeros([N, M])
        #self.Z = np.zeros([N, M])
