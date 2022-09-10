import pickle
from typing import Dict, Any
import matplotlib.pyplot as plt


def flatten(xss):
    """Given a list with 1 or more arrays of arrays, flatten them to a single array"""
    return [x for xs in xss for x in xs]


def loadall(filepath):
    """Load a pickle file by passing in its absolute file path"""
    with open(filepath, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def debug_print_list(list):
    print(*list(list), sep="\n")


def frequency_histogram(
    data: Dict[Any, Any], title: str, xlabel: str, ylabel: str, filename: str
):
    values = list(data.keys())
    freqs = list(data.values())
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.bar(values, freqs, color="blue")
    plt.savefig(filename)
    plt.show()
