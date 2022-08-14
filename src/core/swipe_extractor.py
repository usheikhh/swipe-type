import os
from typing import List
from core.json_config import JSON_Config
from core.swipe import Backing_File, Swipe
from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm

THRESHOLD = JSON_Config.time_delta_threshold()


def plot_deltas(list_delta):
    # Plot all the time deltas fro a single swipe
    plt.plot(list_delta, color="magenta", marker="o", mfc="pink")  # plot the data

    plt.xticks(range(0, len(list_delta) + 1, 1))  # set the tick frequency on x-axis

    plt.ylabel("data")  # set the label for y axis
    plt.xlabel("index")  # set the label for x-axis
    plt.title("Time Deltas")  # set the title of the graph
    plt.show()  # display the graph


def unique_words_from_file(path: str):
    # Find all the unique words for a dataset file
    file = open(path, "r", encoding="UTF-8")
    lines = file.readlines()
    search_space = lines[1:]
    found = set()
    for line in search_space:
        word = list(line.split(" "))[10]
        if (
            word != "me"
            and word != "vanke"
            and word != "told"
            and word != "mary"
            and word != "pembina"
            and word != "interactions"
            and word != "haciendo"
            and len(word) >= 3 and word <= 7
        ):
            found.add(word)
    return found


def extract_trajectories(path: str, key: str):
    # Extract all the rows in the dataset file that match a particular word
    file = open(path, "r", encoding="UTF-8")
    lines = file.readlines()
    found = []
    for line in lines:
        word = list(line.split(" "))[10]
        if key == word:
            found.append(line)
    return (found, key)


def write_to_file(data, key):
    # Write all the rows for a particular word key to a separate word level log file
    # data_file = Path(os.path.join(os.getcwd(), "src", "py", "temp", key + ".log"))
    data_file = Path(os.path.join(os.getcwd(), "src", "core", "temp", key + ".log"))
    data_file.touch(exist_ok=True)
    f = open(data_file, "w+", encoding="UTF-8")
    for line in data:
        word = list(line.split(" "))[10]
        if key == word:
            f.write(line)


def extract_timestamps_from_file(path: str, header_present=False):
    # Extract timestamps from a file. These timestamps can either be taken from a dataset
    # file which has a header at the top which can be ignored, or taken from a word log
    # file, which doesn't have a header
    file = open(path, "r", encoding="UTF-8")
    lines = file.readlines()
    timestamps = []
    for line in lines:
        res = list(line.split(" "))[1]
        timestamps.append((res))
    if header_present == True:
        return timestamps[1:]
    elif header_present == False:
        return timestamps


def extract_timestamps_from_lines(lines: List[str]):
    # Given a list of lines from a file, extract timestamps from it
    timestamps = []
    for line in lines:
        res = list(line.split(" "))[1]
        timestamps.append((res))
    return timestamps


def compute_timestamp_deltas(timestamps: List[int]):
    # Given a list of timestamps we can calculate all of the time deltas which
    # can then be used to try and make swipes
    try:
        # print(timestamps)
        curr = int(timestamps[0])
        # print("curr", curr)
        deltas = []
        for i in range(1, len(timestamps)):
            delta = int(timestamps[i]) - curr
            if delta > 0:
                deltas.append(delta)
            curr = int(timestamps[i])
        return deltas
    except ValueError:
        # print(timestamps)
        curr = int(timestamps[1])
        print("curr", curr)
        deltas = []
        for i in range(2, len(timestamps)):
            delta = int(timestamps[i]) - curr
            deltas.append(delta)
            curr = int(timestamps[i])
        return deltas


def precheck_deltas(deltas: List[int]):
    # A helper function to check if any deltas are above a predefined threshold.
    # If no deltas are above the threshold, then we cannot make swipes so we return
    # False so we can ignore it altogether
    for delta in deltas:
        if delta < THRESHOLD:
            continue
        if delta > THRESHOLD:
            return False
    return True


def extract_swipes_indices(deltas: List[int]):
    # A helper function to find the list indices that are above the time delta threshold
    # print("deltas: ", (deltas))
    if precheck_deltas(deltas) == True:
        return None
    return [i for i in range(len(deltas)) if deltas[i] > THRESHOLD]


def into_intervals(indices: List[int]):
    # Make intervals of all the indices above the threshold so those can be used to make swipes
    intervals = []
    # print("Length of indices: ", len(indices))
    if len(indices) == 0:
        raise ValueError("No indices provided")
    elif len(indices) == 1:
        if indices[0] == 0:
            interval = [0, indices[0] + len(indices) + 1]
        else:
            interval = [0, indices[0] + 1]
        intervals.append(interval)
        return intervals
    try:
        for i in range(0, len(indices)):
            # FIXME: So let's say our indices are: [0, 22, 44], the code currently returns [0, 22], [22, 44]] when instead it should return [0, 22], [23, 44]]
            s = [indices[i], indices[i + 1] + 1]
            intervals.append(s)
        return intervals
    except IndexError:
        return intervals


def create_swipes(timestamps: List[str], word: str, intervals, path: str):
    # Create swipes from a list of timestamps, corresponding indices that can be used,
    # and the word being swiped.
    # print(intervals)
    ranges = []
    for interval in intervals:
        ranges.append(list(range(interval[0], interval[1] + 1)))
    # print(ranges)
    swipe_list = []
    times = []
    for index_range in ranges:
        for element in index_range:
            time = timestamps[element - 1]
            times.append(time)
        swipe = Swipe(word, Backing_File(path), times)
        # print(len(times))
        # print(swipe)
        swipe_list.append(swipe)
        # print(len(swipe_list))
        # Clear the existing times before iterating again
        times = []
    return swipe_list


def write_all_word_logs():
    # Write all the trajectories for all the words at one time
    p = os.path.join(os.getcwd(), "data")
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        # print(file)
        words = unique_words_from_file(os.path.join(os.getcwd(), "data", file))
        # print(words)
        for unique_word in words:
            # At this current moment we can reasonably assume that all the files have been generated
            trajectories, word = extract_trajectories(
                os.path.join(os.getcwd(), "data", file),
                unique_word,
            )
            write_to_file(trajectories, unique_word)
