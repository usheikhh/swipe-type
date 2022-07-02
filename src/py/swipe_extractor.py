import pandas as pd
import os
from typing import List
from swipe import Swipe

THRESHOLD = 30


def grab_first():
    path = os.path.join(os.getcwd(), "data")
    first = os.listdir(path)[0]
    print(first)
    pd.options.display.max_columns = None
    df = pd.read_csv(os.path.join(path, first))
    return df


def unique_words(df: pd.DataFrame):
    data = df.iloc[:, :1].values.tolist()
    store = []
    for row in data:
        # Since the log file is not actually a csv we can't do a simple column name/index lookup
        string = row[10]
        sep = " "
        # Use a regex of the space character to split out the sentence column from the string
        sentence = string.split(sep, 1)[0]
        store.append(sentence)
    return set(store)


def unique_sentences(df: pd.DataFrame):
    data = df.iloc[:, :1].values.tolist()
    store = []
    for row in data:
        # Since the log file is not actually a csv we can;t do a simple column name/index lookup
        string = row[0]
        sep = " "
        # Use a regex of the space character to split out the sentence column from the string
        sentence = string.split(sep, 1)[0]
        store.append(sentence)
    return set(store)


def extract_timestamps(path: str):
    file = open(path, "r")
    lines = file.readlines()
    timestamps = []
    for line in lines:
        res = list(line.split(" "))[1]
        word = list(line.split(" "))[10]
        timestamps.append((res))
    return (timestamps[1:], word)


def compute_timestamp_deltas(timestamps: List[int]):
    curr = int(timestamps[0])
    # print("curr", curr)
    deltas = []
    for i in range(1, len(timestamps)):
        delta = int(timestamps[i]) - curr
        deltas.append(delta)
        curr = int(timestamps[i])
    return deltas


def extract_swipes_indices(deltas: List[int]):
    above = []
    for i in range(0, len(deltas)):
        if deltas[i] >= THRESHOLD:
            above.append(i)
    return above


def into_intervals(indices: List[int]):
    intervals = []
    if len(indices) == 0:
        raise ValueError("No indices provided")
    if len(indices) == 1:
        interval = [0, indices[0]]
        intervals.append(interval)
        return intervals
    starting_index = 0
    for index in indices:
        interval = [starting_index, index]
        intervals.append(interval)
        starting_index = index + 1
    return intervals


def create_swipes(timestamps: List[str], word: str, intervals):
    ranges = []
    for interval in intervals:
        ranges.append(list(range(interval[0], interval[1] + 1)))
    # print(ranges)
    swipe_list = []
    times = []
    for index_range in ranges:
        for element in index_range:
            time = timestamps[element]
            times.append(time)
        swipe = Swipe(word, times)
        # print(len(times))
        # print(swipe)
        swipe_list.append(swipe)
        # print(len(swipe_list))
        # Clear the existing times before iterating again
        times = []
    return swipe_list
