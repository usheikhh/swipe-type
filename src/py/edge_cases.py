import os
import warnings
from features import Feature_Extractor
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


def swipe_coordinates():
    swipe_counter = 1
    timestamps, word = extract_timestamps_from_file(
        os.path.join(os.getcwd(), "src", "py", "delay.log")
    )
    # print("Original:", timestamps)
    delta = compute_timestamp_deltas(timestamps)
    plot_deltas(delta)
    # print("Delta:", delta)
    indices = extract_swipes_indices(delta)
    print("Indices:", indices)
    intervals = into_intervals(indices)
    print("Intervals:", intervals)
    swipes = create_swipes(
        timestamps,
        word,
        intervals,
        os.path.join(os.getcwd(), "src", "py", "delay.log"),
    )
    for swipe in swipes:
        # print(swipe.stringify())
        times = swipe.swipe_timestamps()
        bounds = [swipe.first_and_last_timestamp()]
        for bound in bounds:
            print("Swipe " + str(swipe_counter))
            print("Bound " + str(bound))
            lower = bound[0]
            upper = bound[1]
            # print(lower, upper)
            print("Lower x coordinate", swipe.x_pos(lower))
            print("Lower y coordinate", swipe.y_pos(lower))
            print("Upper x coordinate", swipe.x_pos(upper))
            print("Upper y coordinate", swipe.y_pos(upper))
            swipe_counter += 1
    for swipe in swipes:
        print(Feature_Extractor.length(swipe))


if __name__ == "__main__":
    swipe_coordinates()
