import pandas as pd
import os
from typing import List
from swipe import Backing_File, Swipe
from pathlib import Path

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


def unique_words_from_file(path: str):
    file = open(path, "r")
    lines = file.readlines()
    search_space = lines[1:]
    found = []
    for line in search_space:
        word = list(line.split(" "))[10]
        if word != "me" and word != "vanke" and word != "told":
            found.append(word)
    return set(found)


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


def extract_trajectories(path: str, key: str):
    file = open(path, "r")
    lines = file.readlines()
    found = []
    for line in lines:
        word = list(line.split(" "))[10]
        if key == word:
            found.append(line)
    return (found, key)


def write_to_file(data, key):
    data_file = Path(os.path.join(os.getcwd(), "src", "py", "temp", key + ".log"))
    data_file.touch(exist_ok=True)
    f = open(data_file, "w+")
    for line in data:
        word = list(line.split(" "))[10]
        if key == word:
            f.write(line)


def extract_timestamps_from_file(path: str, header_present=False):
    file = open(path, "r")
    lines = file.readlines()
    timestamps = []
    for line in lines:
        res = list(line.split(" "))[1]
        word = list(line.split(" "))[10]
        timestamps.append((res))
    if header_present == True:
        return (timestamps[1:], word)
    if header_present == False:
        return (timestamps, word)


def extract_timestamps_from_lines(lines: List[str]):
    timestamps = []
    for line in lines:
        res = list(line.split(" "))[1]
        word = list(line.split(" "))[10]
        timestamps.append((res))
    return (timestamps, word)


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


def create_swipes(timestamps: List[str], word: str, intervals, path: str):
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
        swipe = Swipe(word, Backing_File(path), times)
        # print(len(times))
        # print(swipe)
        swipe_list.append(swipe)
        # print(len(swipe_list))
        # Clear the existing times before iterating again
        times = []
    return swipe_list
