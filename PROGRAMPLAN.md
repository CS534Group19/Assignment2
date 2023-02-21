# **Assignment 2**
## Helpful Resources for Python Gridworlds
1. [Gridworld in Python RL](https://realdiganta.medium.com/coding-the-gridworld-example-from-deepminds-reinforcement-learning-course-in-python-17d74335fcbc)
2. [Gridworld RL](https://towardsdatascience.com/reinforcement-learning-implement-grid-world-from-scratch-c5963765ebff) 
3. [Q-Learning](https://towardsdatascience.com/simple-reinforcement-learning-q-learning-fcddc4b6fe56)
4. [SARSA Learning](https://www.geeksforgeeks.org/sarsa-reinforcement-learning/)
## **Checklist**
- [ ] Part 1: Deterministic Actions with Epsilon Exploration
- [ ] 1.1: Gridworld made
- [ ] 1.2:  
- [ ] 1.3:  
- [ ] Part 2: Alter determinism to non-deterministic parameters
- [ ] 2.1: 
- [ ] 2.2:  
- [ ] 2.3:  
- [ ] Part 3: Adjusting for NxN size for better exploration
- [ ] 3.1: 
- [ ] 3.2:  
- [ ] 3.3:  
- [ ] Part 4: Accounting for Time
- [ ] 4.1: 
- [ ] 4.2:  
- [ ] 4.3:  

## Roadmap for Program
1. Develop gridworld 'universe'
2. Develop grid block design
### Develop Gridworld 'Universe'
1. .txt reader to gridworld. Numpy anyone?
2. Grid-world ===> an nxn world of grid blocks
### Develop Grid Block Design
1. Grid Block Data Structure (X, Y, ..., ..., etc) & (TimesVisited)
2. Print Gridworld function (to .txt and/or console)
### Develop Gridworld Physics
1. How to make transition model ===> (0,1,2,3,4) for (crash,up,down,left,right)? [action a as an int move from state s]?
### Sanity Check
1. Program revolves around:
    **1. filename** 
    **2. timeToRun [0.25, 20]**
    **3. actionReward (-∞, 0)**
    **4. pSuccess (0, 1]**
    **5. timeBasedTF**
2. Implement 1-4 first
3. *Implementation of 5 will come in part 4*
### Assignment
- Part 1: Deterministic Actions with Epsilon Exploration
    1. Pseudocode:
    >'
    **determineAction(s):**
        if rand() < epsilon
            return SOME ACTION
        else 
            return action w/ highest Q(s,a) value
    
    **takeAction(s, a):**
        **Transition Model**
        if pSuccess = 1
            Perform action correctly
        else 
            >>"Magic 8-Ball, did I get there?" 
            >>"Concentrate and ask again"

    **update(s, a, s'):**
        Dependent on SARSA or Q-Learning???
        SARSA --> Q(st,at) ← Q(st,at)+α[ rt+1+γV(st+1)−Q(st,at) ]
        Q-Learning --> Q[state, action] = Q[state, action] + lr * (reward + gamma * np.max(Q[new_state, :]) — Q[state, action])

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
    '>
    2. Calculate simple Π* 
        1. Examine each gridworld block
        2. Direction of greatest value denotes direction
        3. Symbols ==> (<, >, V, ^)
- Part 2: Alter determinism to non-deterministic parameters
    1. Alter takeAction() with new transition model parameter 
- Part 3: Adjusting for NxN size for better exploration
    1. Experiment with Epsilon Decay???
    2. Threshold cutoff for duplicate moves???
    3. Confidence Intervals???
    4. Q-Tables???
- Part 4: Accounting for Time
    1. Avoid more costs for less reward???
    2. On first 'x' iterations, calculate the average time in ms it takes to make a move???