# Author: Cutter Beck
# Last Edited: 3/14/23
# Editted by Edward Smith, Mike Alicea

from threading import Thread
from time import sleep, perf_counter
import time
from gridworld import *
import numpy as np
import csv
import sys
import os

np.set_printoptions(linewidth=300)
np.set_printoptions(precision=3, suppress=True)
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

# TODO: REMOVE BEFORE TURNING IN
# For commandline testing
EPSILON = float(sys.argv[6])

# For actual runs
BOARD = sys.argv[1]
RUN_TIME = float(sys.argv[2])
ACTIONREWARD = float(sys.argv[3])
PSUCCESS = float(sys.argv[4])
TIMEBASEDTF = sys.argv[5]

# UPDATE the below variables
ISGREEDY = False
NEGLIGIBLE = 0.18

# EPSILON = 0.8

test_data = gridFileRead(BOARD)

grid_world = Gridworld(test_data, EPSILON, ACTIONREWARD, PSUCCESS)
# STATE SHOULD BE AN X & Y pair cartesian coordinate tuple

ISCURIOUS = False           # Set to true when gates exist
if list(zip(*np.where(grid_world.grid[0].isalpha() and grid_world.grid[0] != "S")))[0]:
    ISCURIOUS = True
    grid_world.ALPHA = 0.2
    grid_world.GAMMA = 1

raw_rewards = []

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
    begin = perf_counter()
    counter = 0
    startTime = time.time()

    while True:
        global stop_threads
        if stop_threads:
            break
        start_state = grid_world.start
        grid_world.grid[1] = grid_world.grid[0]
        current_state = start_state
        trial_reward = 0
        # while not a terminal
        while True:
            grid_world.grid[2][current_state[0]][current_state[1]] = str(
                int(grid_world.grid[2][current_state[0]][current_state[1]]) + 1)

            if grid_world.grid[1][current_state[0]][current_state[1]] not in POSSIBLE_TERMINALS:
                action = grid_world.determineAction(current_state)
                state_prime = grid_world.takeAction(current_state, action)
                action_prime = grid_world.determineAction(state_prime)
                move_reward = grid_world.update(current_state, action,
                                                state_prime, action_prime)
                trial_reward += move_reward

                current_state = state_prime

                counter += 1

                if counter % 10000 == 0:
                    policy = grid_world.calcAndReportPolicy()  # Broken because of QGrid
                    heatmap = grid_world.calcAndReportHeatmap()
                    qgrid = grid_world.QGrid
                    counts = grid_world.reportCounts()  # Broken because of

                    print("**************************** Policy No. ",
                          counter / 10000, "****************************")
                    print(policy)
                    print()

                    
                    print("**************************** Q Grid No. ",
                        counter / 10000, "****************************")
                    print(qgrid)
                    print()
                    

                    print("**************************** Heatmap No. ",
                          counter / 10000, "****************************")
                    print(heatmap)
                    print()

                    print("**************************** Count Grid No. ",
                          counter / 10000, "****************************")
                    print(counts)
                    print()

                    print("**************************** Epsilon Value ",
                        counter / 10000, "****************************")
                    print(grid_world.EPSILON)
                    print()


            else:
                grid_world.update(current_state, action, state_prime, action_prime)
                break

        current_time = perf_counter()
        raw_rewards.append((current_time - begin, trial_reward))

        if not ISGREEDY:
            if ISCURIOUS:
                grid_world.EPSILON *= 0.999
            else:
                grid_world.EPSILON *= 0.99
            if grid_world.EPSILON < NEGLIGIBLE:
                grid_world.EPSILON = 0

        if TIMEBASEDTF == "True":
            if time.time() - startTime > RUN_TIME * 0.90:
                grid_world.EPSILON = 0.0
                ########################################################
                if ISCURIOUS:
                    grid_world.ALPHA *= 0.99
                    if (grid_world.ALPHA < 0.1):
                        grid_world.ALPHA = 0.1
                    grid_world.GAMMA *= 0.99
                    if (grid_world.GAMMA < 0.9):
                        grid_world.GAMMA = 0.9
                ########################################################

        
# Creates a daemon thread to run in the background of the main thread
# This allows for predictable time constraints
stop_threads = False
run = Thread(target=main)
run.daemon = True
run.start()
# sleep(RUN_TIME) silences the main thread for the specified amount of time, and after that amount of time, the daemon thread is also killed
sleep(RUN_TIME)
stop_threads = True
run.join()
# print("\n##### Program Ending... ignore coming error. Daemon thread being shut down.\n")

Assignment2Dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
with open(f"{Assignment2Dir}/documentation/RawReward{EPSILON}.csv", "w", newline="") as raw:
    csv_writer = csv.writer(raw, delimiter=",")
    csv_writer.writerow(["Time", "Reward"])
    for point in raw_rewards:
        csv_writer.writerow([point[0], point[1]])
