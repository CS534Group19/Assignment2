import subprocess
import os
import csv
import matplotlib.pyplot as plt
from time import sleep
import numpy as np

# Starting constants
BOARD = "../documentation/test_boards/intermediate.txt"
TIME = 0.5
ACTIONREWARD = -0.04
PSUCCESS = 0.7
TIMEBASED = False
EPSILON = 1.0
ALPHA = 0.9
GAMMA = 0.9

# UPDATE this variable
REPORT_INTERVAL = 0.04  # 100 ms
DECAY = True

Assignment2Dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
DATA_DIR = f"{Assignment2Dir}\\documentation\\RawData"
AVERAGE_DIR = f"{Assignment2Dir}\\documentation\\Averages"


def clear_data():
    # Clear Raw Data
    for filename in os.listdir(DATA_DIR):
        f = os.path.join(DATA_DIR, filename)
        # checking if it is a file
        if os.path.isfile(f):
            os.remove(f)

    # Clear Averages folder
    for filename in os.listdir(AVERAGE_DIR):
        f = os.path.join(AVERAGE_DIR, filename)
        # checking if it is a file
        if os.path.isfile(f):
            os.remove(f)


def load_data():
    # Load in raw data and calculate the average reward
    for filename in os.listdir(DATA_DIR):
        f = os.path.join(DATA_DIR, filename)
        # checking if it is a file
        if os.path.isfile(f):
            epsilon_val = f.split('-')[1]
            alpha_val = f.split('-')[2]
            gamma_val = f.split('-')[3]

            raw_values = []
            average_rewards = []
            # Load raw data
            with open(f, 'r') as raw:
                csv_reader = csv.reader(raw, delimiter=',')
                line_counter = 0
                for row in csv_reader:
                    if line_counter != 0:
                        point = (row[0], row[1])
                        raw_values.append(point)
                    line_counter += 1

            # Calculate Average Rewards
            counter = 0
            total_reward: float = 0.0
            for point in raw_values:
                total_reward += float(point[1])
                counter += 1
                if len(average_rewards) > 0:
                    if float(point[0]) - average_rewards[-1][0] >= REPORT_INTERVAL:
                        average_rewards.append(
                            (float(point[0]), total_reward / counter))
                else:
                    average_rewards.append(
                        (float(point[0]), total_reward / counter))

            # Write the average rewards to a CSV associated with the Epsilon value
            with open(f"../documentation/Averages/AverageReward-{epsilon_val}-{alpha_val}-{gamma_val}-.csv", "w", newline="") as average:
                csv_writer = csv.writer(average, delimiter=",")
                for point in average_rewards:
                    csv_writer.writerow([point[0], point[1]])


def plot_data(plot_name: str):
    # Plot the averages
    figure = plt.figure()
    axis = figure.add_subplot(111)

    file_data = []
    for filename in os.listdir(AVERAGE_DIR):
        f = os.path.join(AVERAGE_DIR, filename)
        # checking if it is a file
        if os.path.isfile(f):
            current_data = [filename.split('-')[1:-1]]
            with open(f, 'r') as average:
                csv_reader = csv.reader(average, delimiter=",")
                counter = 0
                for row in csv_reader:
                    if counter != 0:
                        point = (float(row[0]), float(row[1]))
                        current_data.append(point)
                    counter += 1
            file_data.append(current_data)

    # Defines a class to hold each set of averages computed from the raw data

    class Trial():
        def __init__(self, epsilon, alpha, gamma, x, y):
            self.epsilon = epsilon
            self.alpha = alpha
            self.gamma = gamma
            self.x = x
            self.y = y
            self.equation = self.get_equation()

        def get_equation(self):
            return np.polyfit(self.x, self.y, 2)

    # All the averages
    fits: list[Trial] = []

    # Load in data points to plot all relevant averages
    for data in file_data:
        x = []
        y = []
        counter = 0
        label: str
        for point in data:
            if counter == 0:
                label = point
            else:
                x.append(point[0])
                y.append(point[1])
            counter += 1

        slope = y[1] - y[0]
        if slope >= 0:
            axis.scatter(x, y, label=label, s=3)
            current_trial = Trial(float(label[0]), float(
                label[1]), float(label[2]), x, y)
            fits.append(current_trial)

    # Find the mean function of all plotted trials
    average_y = []
    fit_counter = 0
    epsilon_sum = 0.0
    alpha_sum = 0.0
    gamma_sum = 0.0

    # Find fit with fewest y vals
    min = len(fits[0].y)
    for fit in fits:
        if len(fit.y) < min:
            min = len(fit.y)

    for fit in fits:
        epsilon_sum += fit.epsilon
        alpha_sum += fit.alpha
        gamma_sum += fit.gamma
        if len(average_y) == 0:
            for i in range(min):
                average_y.append(fit.y[i])
        else:
            for i in range(min):
                average_y[i] += fit.y[i]
        fit_counter += 1
    average_y = [y/fit_counter for y in average_y]
    x_vals = [fits[0].x[i] for i in range(min)]
    axis.plot(x_vals, average_y)

    axis.set_title(
        f"Average Trial Reward vs Time\nEpsilon: {round(epsilon_sum/fit_counter, 2)} Alpha: {round(alpha_sum/fit_counter, 2)}, Gamma: {round(gamma_sum/fit_counter, 2)}")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Average Reward")
    axis.grid(True)
    # plt.legend(loc="lower right")
    plt.savefig(f"../documentation/{plot_name}.png")
    return (round(epsilon_sum/fit_counter, 2), round(alpha_sum/fit_counter, 2), round(gamma_sum/fit_counter, 2))


# Run the actual tests
clear_data()
epsilon = EPSILON
for i in range(20):
    subprocess.call(
        f"python main.py {BOARD} {TIME} {ACTIONREWARD} {PSUCCESS} {TIMEBASED} {epsilon} {ALPHA} {GAMMA}", shell=True)
    epsilon -= 0.05
load_data()
epsilon_average = plot_data("epsilon_test")[0]

clear_data()
alpha = ALPHA
for i in range(18):
    subprocess.call(
        f"python main.py {BOARD} {TIME} {ACTIONREWARD} {PSUCCESS} {TIMEBASED} {EPSILON} {alpha} {GAMMA}", shell=True)
    alpha -= 0.05
load_data()
alpha_average = plot_data("alpha_test")[1]

clear_data()
gamma = GAMMA
for i in range(18):
    subprocess.call(
        f"python main.py {BOARD} {TIME} {ACTIONREWARD} {PSUCCESS} {TIMEBASED} {EPSILON} {ALPHA} {gamma}", shell=True)
    gamma -= 0.05
load_data()
gamma_average = plot_data("gamma_test")[2]

print(epsilon_average, alpha_average, gamma_average)
