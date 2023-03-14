# Author: Cutter Beck
# Last Edited: 3/1/23
# Editted by Edward Smith, Mike Alicea

import numpy as np
np.set_printoptions(precision=3, suppress=True)
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

from gridworld import *
from time import sleep
from threading import Thread
import time

# time to run the program in seconds
EPSILON = 0.8
ACTIONREWARD = -0.1
PSUCCESS = 1
RUN_TIME = 5
ISGREEDY = False

# Test 1
test_file = "./documentation/test_boards/fattysausagegrid.txt"
test_data = gridFileRead(test_file)

grid_world = Gridworld(test_data, EPSILON, ACTIONREWARD, PSUCCESS)
# STATE SHOULD BE AN X & Y pair cartesian coordinate tuple

# TODO refactor Gridworld constants to be read from commandline

def main():  # Cutter Beck
    """
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
    counter = 0
    startTime = time.time()

    while True:
        start_state = grid_world.start
        grid_world.grid[1] = grid_world.grid[0]
        current_state = start_state
        # while not a terminal
        while True:
            grid_world.grid[2][current_state[0]][current_state[1]] = str(
                    int(grid_world.grid[2][current_state[0]][current_state[1]]) + 1)
            
            if grid_world.grid[1][current_state[0]][current_state[1]] not in POSSIBLE_TERMINALS:
                action = grid_world.determineAction(current_state)
                state_prime = grid_world.takeAction(current_state, action)
                action_prime = grid_world.determineAction(state_prime)
                grid_world.update(current_state, action, state_prime, action_prime)

                current_state = state_prime

                counter += 1

                if counter % 10000 == 0:
                    policy = grid_world.calcAndReportPolicy()  # Broken because of QGrid
                    qgrid = grid_world.QGrid
                    heatmap = grid_world.calcAndReportHeatmap()
                    counts = grid_world.reportCounts()  # Broken because of

                    print("**************************** Policy No. ",
                        counter / 1000, "****************************")
                    print(policy)
                    print()

                    print("**************************** Heatmap No. ",
                        counter / 1000, "****************************")
                    print(heatmap)
                    print()

                    print("**************************** Count Grid No. ",
                        counter / 1000, "****************************")
                    print(counts)
                    print(grid_world.EPSILON)

            else:
                break

        

        
        

        if not ISGREEDY:
            if grid_world.EPSILON > 0.6:
                grid_world.EPSILON *= 0.985
            elif grid_world.EPSILON > 0.4:
                grid_world.EPSILON *= 0.99
            elif grid_world.EPSILON < 0.2:
                grid_world.EPSILON = 0

        else:
            if time.time() - startTime > RUN_TIME*0.9:
                grid_world.EPSILON = 0
            else:
                grid_world.EPSILON *= 1-0.001*(time.time()-startTime)/(RUN_TIME*RUN_TIME)
        

# Creates a daemon thread to run in the background of the main thread
# This allows for predictable time constraints
run = Thread(target = main)
run.daemon = True
run.start()
# sleep(RUN_TIME) silences the main thread for the specified amount of time, and after that amount of time, the daemon thread is also killed
sleep(RUN_TIME)
print("\n##### Program Ending... ignore coming error. Daemon thread being shut down.\n")
