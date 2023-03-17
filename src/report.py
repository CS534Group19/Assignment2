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

# UPDATE this variable
REPORT_INTERVAL = 0.05  # 100 ms

Assignment2Dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
DIR = f"{Assignment2Dir}\\documentation\\Averages"

# python main.py "D:/WPI/Sophomore Year/CS534/Assignment2/documentation/test_boards/fattysausagegrid.txt" 1 -0.4 0.7 False 0.8

# Clear Averages folder
for filename in os.listdir(DIR):
    f = os.path.join(DIR, filename)
    # checking if it is a file
    if os.path.isfile(f):
        os.remove(f)


def find_run_average(EPSILON):
    raw_values = []
    average_rewards = []
    # Load raw data
    with open(f"../documentation/RawReward{EPSILON}.csv", 'r') as raw:
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
    with open(f"../documentation/Averages/AverageReward-{EPSILON}-.csv", "w", newline="") as average:
        csv_writer = csv.writer(average, delimiter=",")
        for point in average_rewards:
            csv_writer.writerow([point[0], point[1]])

# Find averages for specified EPSILON values
for i in range(len(sys.argv)):
    if i > 0:
        find_run_average(float(sys.argv[i]))

# Plot the averages
figure = plt.figure()
axis = figure.add_subplot(111)

file_data = []
for filename in os.listdir(DIR):
    f = os.path.join(DIR, filename)
    # checking if it is a file
    if os.path.isfile(f):
        current_data = [filename]
        with open(f, 'r') as average:
            csv_reader = csv.reader(average, delimiter=",")
            for row in csv_reader:
                point = (float(row[0]), float(row[1]))
                current_data.append(point)
        file_data.append(current_data)

for data in file_data:
    x = []
    y = []
    counter = 0
    label: str
    for point in data:
        if counter == 0:
            label = point
            label = label.split("-")[1]
        else:
            x.append(point[0])
            y.append(point[1])
        counter += 1
    axis.scatter(x, y, label=label, s=3)

plt.legend(loc="lower right")
plt.savefig("../documentation/average_rewards.png")
