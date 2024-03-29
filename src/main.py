# Author: Cutter Beck
# Last Edited: 3/14/23
# Editted by Edward Smith, Mike Alicea

import threading
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


EPSILON = 0.73
ALPHA = 0.58
GAMMA = 0.9

# For actual runs
BOARD = sys.argv[1]
RUN_TIME = float(sys.argv[2])
ACTIONREWARD = float(sys.argv[3])
PSUCCESS = float(sys.argv[4])
TIMEBASEDTF = sys.argv[5]

# UPDATE the below variables
ISGREEDY = False
NEGLIGIBLE = 0.18

test_data = gridFileRead(BOARD)

grid_world = Gridworld(test_data, EPSILON, ACTIONREWARD, PSUCCESS)
# STATE SHOULD BE AN X & Y pair cartesian coordinate tuple

ISCURIOUS = True           # Set to true when gates exist

'''
if list(zip(*np.where(grid_world.grid[0] and grid_world.grid[0] != "S")))[0]:
    ISCURIOUS = True
if list(zip(*np.where(grid_world.grid[0] == "+" or grid_world.grid[0] == "-")))[0]:
    ISCURIOUS = True
'''

# if ISCURIOUS == True:
grid_world.ALPHA = ALPHA
grid_world.GAMMA = GAMMA

raw_rewards = []

class AgentThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

    def run(self):
        lock = threading.Lock()
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

        largestTerminalStateReachSoFar = -10.0
        distanceToLargestTerminal = float(-100000)
        RISK_THRESHOLD = 1

        with lock:
            while not self._stop_event.is_set():
                start_state = grid_world.start
                grid_world.grid[1] = grid_world.grid[0]
                current_state = start_state
                trial_reward = 0
                distanceTraveled = 0
                # while not a terminal
                while True:
                    grid_world.grid[2][current_state[0]][current_state[1]] = str(
                        int(grid_world.grid[2][current_state[0]][current_state[1]]) + 1)

                    if grid_world.grid[1][current_state[0]][current_state[1]] not in POSSIBLE_TERMINALS:
                        action = grid_world.determineAction(current_state)
                        state_prime = grid_world.takeAction(current_state, action)
                        action_prime = grid_world.determineAction(state_prime)
                        move_reward = grid_world.update(current_state, action,
                                                        state_prime, action_prime, False)
                        trial_reward += move_reward

                        distanceTraveled += 1

                        current_state = state_prime

                        counter += 1

                    else:
                        grid_world.update(current_state, action, state_prime, action_prime, False)
                        distanceTraveled += 1
                        X, Y = current_state
                        if largestTerminalStateReachSoFar < float(grid_world.grid[0][X][Y]):
                            largestTerminalStateReachSoFar = float(grid_world.grid[0][X][Y])
                            distanceToLargestTerminal = distanceTraveled
                        if largestTerminalStateReachSoFar > float(grid_world.grid[0][X][Y]):
                            grid_world.update(current_state, action, state_prime, action_prime, True)
                        break

                current_time = perf_counter()
                raw_rewards.append((current_time - begin, trial_reward))

                if not ISGREEDY:
                    if ISCURIOUS == True:
                        grid_world.EPSILON *= 0.999
                    else:
                        grid_world.EPSILON *= 0.99
                    if grid_world.EPSILON < NEGLIGIBLE:
                        grid_world.EPSILON = 0

                ########################################################
                if ISCURIOUS == True:
                    grid_world.ALPHA *= 0.9999
                    if (grid_world.ALPHA < 0.1):
                        grid_world.ALPHA = 0.1
                    grid_world.GAMMA *= 0.9999
                    if (grid_world.GAMMA < 0.9):
                        grid_world.GAMMA = 0.9
                ########################################################

                if TIMEBASEDTF == "True":
                        RISK_THRESHOLD = RISK_THRESHOLD * (time.time() - startTime) / RUN_TIME
                        if ((largestTerminalStateReachSoFar - (distanceToLargestTerminal * 0.04))/ grid_world.worldSize < RISK_THRESHOLD):
                          grid_world.EPSILON = grid_world.EPSILON * 1.02
                          grid_world.GAMMA = grid_world.GAMMA * 1.05

                          if grid_world.EPSILON > 1:
                            grid_world.EPSILON = 1

                          if grid_world.GAMMA > 0.9:
                            grid_world.GAMMA = 0.9

                        if time.time() - startTime > RUN_TIME * 0.90:
                            grid_world.EPSILON = 0
                    
    def stop(self):
        self._stop_event.set()
        
# Creates a daemon thread to run in the background of the main thread
agent = AgentThread()
agent.daemon = True
print(f"Please wait {RUN_TIME} seconds...")
agent.start()
# sleep(RUN_TIME) silences the main thread for the specified amount of time, and after that amount of time, the daemon thread is also killed
sleep(RUN_TIME)
agent.stop()
agent.join()

policy = grid_world.calcAndReportPolicy()  # Broken because of QGrid
heatmap = grid_world.calcAndReportHeatmap()
qgrid = grid_world.QGrid
counts = grid_world.reportCounts()  # Broken because of

print("\nPolicy")
print(policy)

print("\nHeatmap")
print(heatmap)

Assignment2Dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
with open(f"{Assignment2Dir}/documentation/RawData/RawReward-{round(EPSILON, 2)}-{round(grid_world.ALPHA, 2)}-{round(grid_world.GAMMA, 2)}-.csv", "w", newline="") as raw:
    csv_writer = csv.writer(raw, delimiter=",")
    csv_writer.writerow(["Time", "Reward"])
    for point in raw_rewards:
        csv_writer.writerow([point[0], point[1]])
