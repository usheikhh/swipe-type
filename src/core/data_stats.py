import os
import statistics
from tqdm import tqdm
from features import Feature_Extractor

from user import User
from util import flatten


timestamps = 0
files = 0


def count_timestamps(header_present=True):
    file_count = 0
    timestamps = []
    p = os.path.join(os.getcwd(), "data")
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        file_count += 1
        f = open(os.path.join(os.getcwd(), "data", file))
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            print(file)
            pass

        for line in lines:
            res = list(line.split(" "))[1]
            timestamps.append(res)
    if header_present == True:
        print(len(timestamps[1:]))


print(count_timestamps())


def extract_timestamps_from_file(path: str, header_present=True):
    file = open(path, "r")
    lines = file.readlines()
    timestamps = []
    for line in lines:
        res = list(line.split(" "))[1]
        word = list(line.split(" "))[10]
        timestamps.append((res))
    if header_present == True:
        return sum(timestamps[1:])
    elif header_present == False:
        return sum(timestamps)


def avg_swipes():
    p = os.path.join(os.getcwd(), "data")
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    file_swipes = []
    for file in tqdm(onlyfiles):
        if file == ".DS_Store":
            pass
        print(file)
        s = 0
        if file == ".log":
            return
        else:
            user = User(
                file,
                os.path.join(os.getcwd(), "data", file),
            )
            for swipe in user.make_all_swipes().items():
                s += 1
        file_swipes.append(s)
        # print(file_swipes)
    return sum(file_swipes) / len(file_swipes)


def average_swipe_length():
    p = os.path.join(os.getcwd(), "data")
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    swipe_lengths = []
    swipes = []
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        swipes.append(user.make_all_swipes())
    flat_swipes = flatten(swipes)
    for swipe in tqdm(flat_swipes):
        swipe_lengths.append(Feature_Extractor.length(swipe))
    avg = sum(swipe_lengths) / len(swipe_lengths)
    st_dev = statistics.stdev(swipe_lengths)
    print("Avg:", avg)
    print("st. dev", st_dev)


if __name__ == "__main__":
    average_swipe_length()
