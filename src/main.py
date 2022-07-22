from rich.traceback import install
from core.features import Feature_Extractor
from core.swipe_extractor import (
    compute_timestamp_deltas,
    extract_timestamps_from_file,
    extract_swipes_indices,
    into_intervals,
    create_swipes,
    unique_words_from_file,
    write_all_word_logs,
)
import os
import pickle
import warnings
from tqdm import tqdm

from core.util import flatten

if __name__ == "__main__":
    install()
    # write_all_word_logs()
    p = os.path.join(os.getcwd(), "data")
    swipeset = []
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        # print(file)
        for unique_word in unique_words_from_file(
            os.path.join(os.getcwd(), "data", file)
        ):
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
                swipeset.append(swipes)
            elif indices is None:
                warnings.warn(
                    "No indices above the threshold, so swipes cannot be made"
                )
    # flat_swipes = flatten(swipeset)
    # for swipe in tqdm(flat_swipes):
    #     (Feature_Extractor.extract_all_features(swipe))
