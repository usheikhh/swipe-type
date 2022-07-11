import os
import warnings
from features import Feature_Extractor
from algo import manhattan, scipy_manhattan
from swipe_extractor import *


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
        first, last = swipe.first_and_last_timestamp()
        print(swipe.get_backing_file().lookup_row_by_timestamp(first))
        # print(last in swipe.swipe_timestamps())
        # print(first in ts, last in ts)
        # ? Why can the row be found.... it's definitely in the file
        # print(row)
        print("First X-Position:", swipe.x_pos(first))
        print("First Y-Position:", swipe.y_pos(first))
        print("Last X-Position:", swipe.x_pos(last))
        print("First Y-Position:", swipe.y_pos(last))
        print(list(Feature_Extractor.extract_all_features(swipe).values()))
        vectors.append(list(Feature_Extractor.extract_all_features(swipe).values()))
    return vectors


def distance_test(fv1, fv2):
    return manhattan(fv1, fv2)


if __name__ == "__main__":
    paths = []
    for file in os.listdir(os.path.join(os.getcwd(), "src", "py")):
        if file.endswith(".log"):
            path = os.path.join(os.getcwd(), "src", "py", file)
            print(path)

        total = 0
        try:
            vector_set1 = zero_division_length_error(
                os.path.join(os.getcwd(), "src", "py", "edwards.log")
            )
        except TypeError:
            print("Failed path: ", path)
    vector_set2 = zero_division_length_error(
        os.path.join(os.getcwd(), "src", "py", "belt.log")
    )
    # for fv in vector_set1:
    #     for fv2 in vector_set2:
    #         total += scipy_manhattan(fv, fv2)
    # print("Total:", total)
