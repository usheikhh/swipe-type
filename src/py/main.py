from features import Feature_Extractor
from swipe_extractor import (
    compute_timestamp_deltas,
    extract_timestamps_from_file,
    extract_swipes_indices,
    into_intervals,
    create_swipes,
    unique_words_from_file,
    extract_trajectories,
    extract_timestamps_from_lines,
    write_to_file,
)
import os
import pickle
import warnings
from tqdm import tqdm

if __name__ == "__main__":
    p = os.path.join(os.getcwd(), "data")
    swipeset = []
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        print(file)
        words = unique_words_from_file(os.path.join(os.getcwd(), "data", file))
        # print(words)
        for unique_word in words:
            # At this current moment we can reasonably assume that all the files have been generated
            # trajectories, word = extract_trajectories(
            #     os.path.join(os.getcwd(), "data", file),
            #     unique_word,
            # )
            # write_to_file(trajectories, unique_word)
            timestamps, word = extract_timestamps_from_file(
                os.path.join(os.getcwd(), "src", "py", "temp", unique_word + ".log")
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
                        os.getcwd(), "src", "py", "temp", unique_word + ".log"
                    ),
                )
                swipeset.append(swipes)
            elif indices is None:
                warnings.warn(
                    "No indices above the threshold, so swipes cannot be made"
                )
    for swipes in swipeset:
        for swipe in swipes:
            print(swipe.get_key())
            Feature_Extractor.extract_all_features(swipe)
    with open("data.pickle", "wb") as handle:
        pickle.dump(swipes, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # timestamps, word = extract_timestamps_from_file(
    #     os.path.join(os.getcwd(), "src", "py", "delay.log")
    # )
    # # print("Original:", timestamps)
    # delta = compute_timestamp_deltas(timestamps)
    # # print("Delta:", delta)
    # indices = extract_swipes_indices(delta)
    # # print("Indices:", indices)
    # intervals = into_intervals(indices)
    # print("Intervals:", intervals)
    # swipes = create_swipes(timestamps, word, intervals)
    # for swipe in swipes:
    #     print(swipe.stringify())
