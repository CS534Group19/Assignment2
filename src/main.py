# Author: Cutter Beck
# Last Edited: 3/1/23
# Editted by Edward Smith, Mike Alicea

from gridworld import *

# Test 1
test_file = "./documentation/test_boards/intermediate.txt"
test_data = gridFileRead(test_file)
print(test_data)

gridWorld = Gridworld(test_data)

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

if __name__ == "__main__":
    main()
