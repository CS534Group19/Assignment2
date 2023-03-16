# Author: Cutter Beck
# Edited: 3/14/2023

# To use, run from src directory and type `python report.py EPSILON`
# ALL CSVs CURRENTLY IN THE Averages WILL BE DELETED AT THE START

# Multiple EPSILON values can be written separated by spaces
# Output CSVs and a graph image titled average_rewards.png will be outputted to the documentation directory

import csv
import matplotlib.pyplot as plt
import os
import subprocess
from time import sleep
import sys
import numpy as np

# UPDATE this variable
REPORT_INTERVAL = 0.1  # 100 ms

Assignment2Dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
DATA_DIR = f"{Assignment2Dir}\\documentation\\RawData"
AVERAGE_DIR = f"{Assignment2Dir}\\documentation\\Averages"

# python main.py "D:/WPI/Sophomore Year/CS534/Assignment2/documentation/test_boards/fattysausagegrid.txt" 1 -0.4 0.7 False 0.8

# Clear Averages folder
for filename in os.listdir(AVERAGE_DIR):
    f = os.path.join(AVERAGE_DIR, filename)
    # checking if it is a file
    if os.path.isfile(f):
        os.remove(f)


def load_data():
    # Load raw data
    for filename in os.listdir(DATA_DIR):
        f = os.path.join(DATA_DIR, filename)
        # checking if it is a file
        if os.path.isfile(f):
            epsilon_val = f.split('-')[1]
            alpha_val = f.split('-')[2]
            gamma_val = f.split('-')[3]

            raw_values = []
            average_rewards = []
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
                    average_rewards.append((float(point[0]), total_reward / counter))

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

    if fits:
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
        axis.plot(x_vals, average_y, label="Average Line")

        axis.set_title(
            f"Average Trial Reward vs Time\nEpsilon: {round(epsilon_sum/fit_counter, 2)} Alpha: {round(alpha_sum/fit_counter, 2)}, Gamma: {round(gamma_sum/fit_counter, 2)}")
        axis.set_xlabel("Time (s)")
        axis.set_ylabel("Average Reward")
        axis.grid(True)
        plt.legend(loc="lower right")
        plt.savefig(f"../documentation/{plot_name}.png")
        return (round(epsilon_sum/fit_counter, 2), round(alpha_sum/fit_counter, 2), round(gamma_sum/fit_counter, 2))

load_data()
plot_data("Multiplot")
