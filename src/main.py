# Author: Cutter Beck
# Last Edited: 3/1/23
# Editted by Edward Smith, Mike Alicea

from gridworld import *
from time import sleep
from threading import Thread

# time to run the program in seconds
RUN_TIME = 1.5

# Test 1
test_file = "./documentation/test_boards/intermediate.txt"
test_data = gridFileRead(test_file)
print(test_data)

grid_world = Gridworld(test_data)

# STATE SHOULD BE AN X & Y pair cartesian coordinate tuple


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
    while True:
        start_state = grid_world.start
        current_state = start_state
        while grid_world.grid[1][current_state[0]][current_state[1]] not in POSSIBLE_TERMINALS:
            action = grid_world.determineAction(current_state)
            state_prime = grid_world.takeAction(current_state, action)
            action_prime = grid_world.determineAction(state_prime)
            grid_world.update(current_state, action, state_prime, action_prime)
            # UPDATE the state counter by 1. HOW?????
            # AAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHH. Fuck this
            # WHY STRING?! YOU ARE _ZEROS_. WHY DO YOU DO THIS GIUSEPPE?!
            grid_world.grid[2][6][4] = int(grid_world.grid[2][6][4]) + 1
            current_state = state_prime
            
            counter += 1
            if counter % 100 == 0:
                policy = grid_world.calcAndReportPolicy()
                heatmap = grid_world.calcAndReportHeatmap()
                counts = grid_world.reportCounts()
                print(policy)
                print(heatmap)
                # AAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHH. Fuck this
                # WHY STRING?! YOU ARE _ZEROS_. WHY DO YOU DO THIS GIUSEPPE?!


# Creates a daemon thread to run in the background of the main thread
# This allows for predictable time constraints
run = Thread(target=main)
run.daemon = True
run.start()
# sleep(RUN_TIME) silences the main thread for the specified amount of time, and after that amount of time, the daemon thread is also killed
sleep(RUN_TIME)
