import warnings
import math
from features import Feature_Extractor
from swipe_extractor import (
    compute_timestamp_deltas,
    create_swipes,
    extract_swipes_indices,
    extract_timestamps_from_file,
    extract_trajectories,
    into_intervals,
    write_to_file,
)
from swipe_extractor import unique_words_from_file
import os
from collections import defaultdict


def make_template(swipes):
    mean_template = [0, 0, 0, 0]
    count = 0
    for feature_set in swipes:
        count += 1
        assert len(feature_set) == 4
        for x in range(0, 4):
            mean_template[x] += feature_set[x]
    for y in range(0, 4):
        mean_template[y] /= count
    return mean_template


class User:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def get_path(self):
        return self.path

    def get_name(self):
        return self.name

    def make_all_swipes(self):
        swipeset = defaultdict(list)
        words = unique_words_from_file(self.get_path())
        for unique_word in words:
            # At this current moment we can reasonably assume that all the files have been generated
            trajectories, word = extract_trajectories(self.get_path(), unique_word)
            write_to_file(trajectories, unique_word)
            timestamps, word = extract_timestamps_from_file(
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
                    word,
                    intervals,
                    os.path.join(
                        os.getcwd(), "src", "core", "temp", unique_word + ".log"
                    ),
                )
                for swipe in swipes:
                    swipeset[word].append(swipe)
            elif indices is None:
                warnings.warn(
                    "No indices above the threshold, so swipes cannot be made"
                )
        return swipeset

    def divide_swipes(self, swipes: defaultdict, swipe_count: int):
        template_size = math.floor(swipe_count * 0.7)
        print("template size:", template_size)
        probe_size = swipe_count - template_size
        print("probe size:", probe_size)
        counter = 0
        template = []
        probe = []

        for v in swipes.values():
            for i in v:
                if counter < template_size:
                    template.append(i)
                    counter += 1
                elif counter >= template_size:
                    probe.append(i)
                    counter += 1

        print("counter:", counter)
        print("length of template list:", len(template))
        print("length of probe list:", len(probe))

        return (template, probe)


if __name__ == "__main__":
    sum = 0
    user = User(
        "2c30a5a6amjsgs1ganoo6kg2lb",
        os.path.join(os.getcwd(), "data", "2c30a5a6amjsgs1ganoo6kg2lb.log"),
    )
    for k, v in user.make_all_swipes().items():
        # print(k)
        sum += len(v)
    print(sum)
    features = []
    sum_swipes = 0
    a, b = user.divide_swipes(user.make_all_swipes(), sum)
    for swipe in a:
        features.append(Feature_Extractor.extract_all_features_to_list(swipe))
    # print(features)
    print(make_template(features))
