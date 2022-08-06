import os
import statistics
from tqdm import tqdm
from core.algo import score_calc
from core.user import make_template, User
from core.features import Feature_Extractor, FeatureType
from collections import Counter
from core.util import flatten, frequency_histogram


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
            for swipe in user.make_all_swipes():
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


def get_velocity_values():
    p = os.path.join(os.getcwd(), "data")
    swipes = []
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        swipes.append(user.make_all_swipes())
    flat = flatten(swipes)
    path = os.path.join(os.getcwd(), "stats", "velocity_stats.txt")
    with open(path, "w+") as f:
        for swipe in flat:
            f.write(f"{Feature_Extractor.calculate_velocity(swipe)}\n")


def get_pairwise_acceleration_values():
    p = os.path.join(os.getcwd(), "data")
    swipes = []
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        swipes.append(user.make_all_swipes())
    flat = flatten(swipes)
    path = os.path.join(os.getcwd(), "stats", "pairwise_acceleration_stats.txt")
    with open(path, "w+") as f:
        for swipe in flat:
            f.write(f"{Feature_Extractor.calculate_pairwise_acceleration(swipe)}\n")


def get_length_values():
    p = os.path.join(os.getcwd(), "data")
    swipes = []
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        swipes.append(user.make_all_swipes())
    flat = flatten(swipes)
    path = os.path.join(os.getcwd(), "stats", "length_stats.txt")
    with open(path, "w+") as f:
        for swipe in flat:
            f.write(f"{Feature_Extractor.length(swipe)}\n")


def get_percentile_velocity_values():
    p = os.path.join(os.getcwd(), "data")
    swipes = []
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        swipes.append(user.make_all_swipes())
    flat = flatten(swipes)
    path = os.path.join(os.getcwd(), "stats", "percentile_stats.txt")
    with open(path, "w+") as f:
        for swipe in flat:
            f.write(f"{Feature_Extractor.percentile_velocity(swipe)}\n")


def count_swipes():
    p = os.path.join(os.getcwd(), "data")
    swipes = []
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        swipes.append(user.make_all_swipes())
    flat = flatten(swipes)
    return len(flat)


def get_deviation_ratio_values():
    p = os.path.join(os.getcwd(), "data")
    swipes = []
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        swipes.append(user.make_all_swipes())
    flat = flatten(swipes)
    path = os.path.join(os.getcwd(), "stats", "deviation_stats.txt")
    with open(path, "w+") as f:
        for swipe in flat:
            f.write(f"{Feature_Extractor.deviation_ratio(swipe)}\n")


def get_all_words():
    path = os.path.join(os.getcwd(), "stats", "wordfreq.txt")
    words = set()
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            word = line.split(" ")[1]
            words.add(word.strip())
    return words


def get_value_counts(feature_type: FeatureType):
    data = []
    if feature_type == FeatureType.LENGTH:
        path = os.path.join(os.getcwd(), "stats", "length_stats.txt")
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                data.append(float(line))
        return (Counter(data).keys(), Counter(data).values())
    elif feature_type == FeatureType.VELOCITY:
        path = os.path.join(os.getcwd(), "stats", "velocity_stats.txt")
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                data.append(float(line))
        return (Counter(data).keys(), Counter(data).values())
    elif feature_type == FeatureType.PERCENTILE:
        path = os.path.join(os.getcwd(), "stats", "percentile_stats.txt")
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                data.append(float(line))
        return (Counter(data).keys(), Counter(data).values())
    elif feature_type == FeatureType.ACCELERATION:
        path = os.path.join(os.getcwd(), "stats", "pairwise_acceleration_stats.txt")
        with open(path, "w+") as f:
            lines = f.readlines()
            for line in lines:
                data.append(float(line))
        return (Counter(data).keys(), Counter(data).values())
    elif feature_type == FeatureType.DEVIATION:
        path = os.path.join(os.getcwd(), "stats", "deviation_stats.txt")
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                data.append(float(line))
        return (Counter(data).keys(), Counter(data).values())


def get_word_length_frequency():
    data = {}
    words = get_all_words()
    counts = Counter(len(word) for word in words)
    for length in range(1, max(counts.keys()) + 1):
        data[length] = counts.get(length, 0)
    frequency_histogram(
        data,
        "Word Length Frequency Distribution",
        "Word Lengths",
        "Frequency",
        "word_len_freqs.png",
    )


if __name__ == "__main__":
    print("Swipe Count:", count_swipes())
