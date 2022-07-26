import warnings
from rich.traceback import install
import pickle
from tqdm import tqdm
import math
import statistics
from core.algo import score_calc
from core.features import Feature_Extractor
from core.swipe_extractor import (
    compute_timestamp_deltas,
    create_swipes,
    extract_swipes_indices,
    extract_timestamps_from_file,
    into_intervals,
    unique_words_from_file,
)
import os

SWIPE_LENGTH_THRESHOLD = 437  # Mean + 1 standard deviation above
install()


def make_template(swipes):
    mean_template = [0, 0, 0, 0]

    for feature_set in swipes:
        assert len(feature_set) == 4
        for x in range(0, 4):
            mean_template[x] += feature_set[x]
    for y in range(0, 4):
        mean_template[y] /= 4

    return mean_template


def process_files():
    p = os.path.join(os.getcwd(), "data")
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    PIK = "genuine.dat"
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        features = []
        a, b = user.divide_swipes(user.make_all_swipes())
        for swipe in a:
            features.append(Feature_Extractor.extract_all_features_to_list(swipe))
        # print(features)
        # print(make_template(features))

        # this prints out all the genuine scores
        genuine_scores = []
        template_features = make_template(features)
        for swipe in b:
            genuine_scores.append(score_calc(template_features, swipe))
        with open(PIK, "ab") as f:
            pickle.dump(genuine_scores, f)
        for impostor_file in tqdm(onlyfiles):
            if impostor_file == file:
                print("SAME FILE REACHED")
                pass
            else:
                impostor_user = User(
                    impostor_file, os.path.join(os.getcwd(), "data", impostor_file)
                )
                impostor_scores = []
                # print(" Genuine scores", genuine_scores)

                # Printing out impostor scores
                other_file_total = impostor_user.make_all_swipes()
                print(" Impostor file swipe count:", len(other_file_total))
                print(impostor_file)
                for swipe in other_file_total:
                    impostor_scores.append(score_calc(template_features, swipe))
                if not os.path.exists(
                    os.path.join(os.getcwd(), "gen", os.path.splitext(file)[0])
                ):
                    os.makedirs(
                        os.path.join(os.getcwd(), "gen", os.path.splitext(file)[0])
                    )
                imposter_file_path = os.path.join(
                    os.getcwd(),
                    "gen",
                    os.path.splitext(file)[0],
                    "imposter_" + impostor_file,
                )
                # print(imposter_file_path)

                with open(imposter_file_path, "ab") as f:
                    pickle.dump(impostor_scores, f)
            # print("impostor scores:\n", impostor_scores)


def stats():
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


def generate_all_genuine_scores():
    p = os.path.join(os.getcwd(), "data")
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        user = User(
            file,
            os.path.join(os.getcwd(), "data", file),
        )
        # print(sum)
        features = []
        a, b = user.divide_swipes(user.make_all_swipes())
        for swipe in a:
            features.append(Feature_Extractor.extract_all_features_to_list(swipe))
        # print(features)
        # print(make_template(features))

        # this prints out all the genuine scores
        genuine_scores = []
        # starting_time = timeit.default_timer()
        template_features = make_template(features)
        # print("Time difference :", timeit.default_timer() - starting_time)
        for swipe in b:
            genuine_scores.append(score_calc(template_features, swipe))
        genuine_file_path = os.path.join(
            os.getcwd(), "genuine_scores", "genuine_" + file
        )
        # print(file)
        try:
            with open(genuine_file_path, "wb") as f:
                pickle.dump(genuine_scores, f)
        except FileNotFoundError:
            pass


class User:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def get_path(self):
        return self.path

    def get_name(self):
        return self.name

    def make_all_swipes(self):
        swipeset = []
        words = unique_words_from_file(self.get_path())
        for unique_word in words:
            timestamps = extract_timestamps_from_file(
                os.path.join(os.getcwd(), "src", "core", "temp", unique_word + ".log")
            )

            # print("New:", timestamps)
            # print(unique_word)
            delta = compute_timestamp_deltas(timestamps)
            # print(delta)
            indices = extract_swipes_indices(delta)
            if indices is not None:
                # print(indices)
                intervals = into_intervals(indices)
                # print(intervals)
                # input()
                swipes = create_swipes(
                    timestamps,
                    unique_word,
                    intervals,
                    os.path.join(
                        os.getcwd(), "src", "core", "temp", unique_word + ".log"
                    ),
                )
                for swipe in swipes:
                    # print("SWIPE COUNT IS:", len(swipes))
                    # print("SWIPE LENGTH IS:", Feature_Extractor.length(swipe))
                    # print("BEFORE HELD SWIPES:", len(swipeset))
                    # input()
                    if Feature_Extractor.length(swipe) >= SWIPE_LENGTH_THRESHOLD:
                        swipeset.append(swipe)
                    # print("AFTER HELD SWIPES:", len(swipeset))
                    # input()
            elif indices is None:
                warnings.warn(
                    "No indices above the threshold, so swipes cannot be made"
                )
        return swipeset

    def divide_swipes(self, swipes: list):
        template_size = math.floor(len(swipes) * 0.7)
        probe_size = len(swipes) - template_size
        print("Swipe Count: ", len(swipes))
        print("template size:", template_size)
        print("probe size:", probe_size)
        template = swipes[:template_size]
        probe = swipes[template_size:]
        return (template, probe)
