
import os

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

clear_data()