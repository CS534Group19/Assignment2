# Author: Cutter Beck
# Last Edited: 3/1/23
# Editted by Edward Smith, Mike Alicea

from gridworld import *
from time import sleep
from threading import Thread

# time to run the program in seconds
RUN_TIME = 1

# Test 1
test_file = "./documentation/test_boards/intermediate.txt"
test_data = gridFileRead(test_file)
print(test_data)

grid_world = Gridworld(test_data)

# STATE SHOULD BE AN X & Y pair cartesian coordinate tuple


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
                if iterations % 100 == 0:
                    policy = calcAndReportPolicy()
                    heatmap = calcAndReportHeatmap()                
                    print(policy)
                    print(heatmap)
    """
    # while True:
    #     start_state = grid_world.coords
        


# Creates a daemon thread to run in the background of the main thread
# This allows for predictable time constraints
run = Thread(target=main)
run.daemon = True
run.start()
# sleep(RUN_TIME) silences the main thread for the specified amount of time, and after that amount of time, the daemon thread is also killed
sleep(RUN_TIME)
