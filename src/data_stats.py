import os
import statistics
from tqdm import tqdm
from core.algo import score_calc
from core.user import make_template, User
from core.features import Feature_Extractor

from core.util import flatten


timestamps = 0
files = 0


def count_timestamps(header_present=True):
    """Count all the timestamps present in each file in the dataset"""
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


def avg_swipes():
    """Count the average number of swipes for all the files in the dataset directory"""
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
    """Get the average swipe length and its standard deviation across all the swipes of all the dataset files"""
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


def stats():
    """Collect some statistics on the genuine scores:
    1) Average
    2) Mean
    3) Median
    4) Standard Deviation
    """
    p = os.path.join(os.getcwd(), "data")
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    genuine_scores = []
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        features = []
        a, b = user.divide_swipes(user.make_all_swipes())

        for swipe in a:
            features.append(Feature_Extractor.extract_all_features_to_list(swipe))

        template_features = make_template(features)
        for swipe in b:
            genuine_scores.append(score_calc(template_features, swipe))

    print("AVG:", sum(genuine_scores) / len(genuine_scores))
    print("Mean:", statistics.mean(genuine_scores))
    print("Median:", statistics.median(genuine_scores))
    print("St. dev:", statistics.stdev(genuine_scores))

    return genuine_scores


def get_velocity_distribution():
    p = os.path.join(os.getcwd(), "data")
    swipes = []
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        swipes.append(user.make_all_swipes())
    print(swipes)


if __name__ == "__main__":
    get_velocity_distribution()
