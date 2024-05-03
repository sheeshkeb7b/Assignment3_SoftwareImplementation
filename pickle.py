import pickle
from main_classes import *
from pickle import load_data

def save_data(data, filename):
    try:
        with open(os.path.join(data_path, filename), 'wb') as dumpf:
            pickle.dump(data, dumpf)
    except Exception as e:
        print("An error occurred while saving the data:", e)


def load_data(filename):
    try:
        with open(os.path.join(data_path, filename), 'rb') as loadf:
            return pickle.load(loadf)
    except FileNotFoundError:
        print("Data file not found. Starting with an empty dataset.")
        return {}
    except Exception as e:
        print("An error occurred while loading the data:", e)
        return {}
