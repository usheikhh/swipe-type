import os
import warnings
from features import *
from algo import manhattan, scipy_manhattan
from swipe_extractor import *
from tqdm import tqdm


def unique_word_test(filename: str):
    return unique_words_from_file(os.path.join(os.getcwd(), "data", filename))


def i_word_test():
    # TODO: This code represents an edge case we have to consider when creating intervals.
    # Since there are only 2 rows in the file When extracting the indices it is technically correct
    # but since we preemptively add 0 to the interval, we get the wrong interval. Instead
    # the simplest solution is to probably when checking if the indices list is length 1,
    # specifically check if the element is 0 and if it is, find the highest line number
    # for the file in question, and use that as the ending index
    timestamps, word = extract_timestamps_from_file(
        os.path.join(os.getcwd(), "src", "py", "temp", "i.log"), False
    )
    print("Original:", timestamps)
    delta = compute_timestamp_deltas(timestamps)
    print("Diff:", delta)
    indices = extract_swipes_indices(delta)
    print(indices)
    intervals = into_intervals(indices)
    print(intervals)
    swipes = create_swipes(
        timestamps,
        word,
        intervals,
        os.path.join(os.getcwd(), "src", "py", "temp", "i.log"),
    )
    for swipe in swipes:
        print(swipe.stringify())


def me_word_test():
    # TODO: We need to gracefully handle the case when none of the time deltas are greater than the threshold so that the rest of the protocol is not run
    # TODO: There is a rudimentary fix in the code for this now, we just need to hook it up so that it knows to skip those files
    timestamps, word = extract_timestamps_from_file(
        os.path.join(os.getcwd(), "src", "py", "temp", "me.log"), False
    )
    print("Original:", timestamps)   
    delta = compute_timestamp_deltas(timestamps)
    print("Diff:", delta)
    indices = extract_swipes_indices(delta)
    print(indices)
    if indices is not None:
        intervals = into_intervals(indices)
        print(intervals)
        swipes = create_swipes(timestamps, word, intervals)
        for swipe in swipes:
            print(swipe.stringify())
    if indices is None:
        warnings.warn("No indices above the threshold, so swipes cannot be made")


def vanke_word_test():
    # TODO: We need to gracefully handle the case when none of the time deltas are greater than the threshold so that the rest of the protocol is not run
    timestamps, word = extract_timestamps_from_file(
        os.path.join(os.getcwd(), "src", "py", "temp", "vanke.log"), False
    )
    print("Original:", timestamps)
    delta = compute_timestamp_deltas(timestamps)
    print("Diff:", delta)


def told_word_test():
    # TODO: We need to gracefully handle the case when none of the time deltas are greater than the threshold so that the rest of the protocol is not run
    timestamps, word = extract_timestamps_from_file(
        os.path.join(os.getcwd(), "src", "py", "temp", "told.log"), False
    )
    print("Original:", timestamps)
    delta = compute_timestamp_deltas(timestamps)
    print("Diff:", delta)


def zero_division_length_error(path: str):
    vectors = []
    timestamps, word = extract_timestamps_from_file(path, False)
    delta = compute_timestamp_deltas(timestamps)
    print("Delta:", delta)
    indices = extract_swipes_indices(delta)
    print("Indices:", indices)
    intervals = into_intervals(indices)
    print("Intervals:", intervals)
    swipes: List[Swipe] = create_swipes(
        timestamps,
        word,
        intervals,
        path,
    )
    for swipe in swipes:
        print(swipe.get_key())
        print(Feature_Extractor.extract_all_features(swipe))
    return vectors


def distance_test(fv1, fv2):
    return manhattan(fv1, fv2)


def full_run():
    p = os.path.join(os.getcwd(), "src", "core", "temp")
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    swipeset = []
    for file in tqdm(onlyfiles):
        timestamps, word = extract_timestamps_from_file(
            os.path.join(os.getcwd(), "src", "core", "temp", file)
        )
        delta = compute_timestamp_deltas(timestamps)
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
                os.path.join(os.getcwd(), "src", "core", "temp", file),
            )
            swipeset.append(swipes)
        elif indices is None:
            warnings.warn("No indices above the threshold, so swipes cannot be made")
    for swipes in tqdm(swipeset):
        for swipe in swipes:
            print(swipe.get_key())
            # print(Feature_Extractor.extract_all_features(swipe))


if __name__ == "__main__":
    p = os.path.join(os.getcwd(), "src", "core", "temp")

    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        zero_division_length_error(
            os.path.join(os.getcwd(), "src", "core", "temp", file)
        )
