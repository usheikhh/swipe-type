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
import warnings

if __name__ == "__main__":
    words = unique_words_from_file(
        os.path.join(os.getcwd(), "data", "7s2subps693a12v4tqom3objuf.log")
    )
    # print(words)
    for unique_word in words:
        trajectories, word = extract_trajectories(
            os.path.join(os.getcwd(), "data", "7s2subps693a12v4tqom3objuf.log"),
            unique_word,
        )
        write_to_file(trajectories, unique_word)
        timestamps, word = extract_timestamps_from_file(
            os.path.join(os.getcwd(), "src", "py", "temp", unique_word + ".log")
        )

        # print("New:", timestamps)
        print(unique_word)
        delta = compute_timestamp_deltas(timestamps)
        # print(delta)
        indices = extract_swipes_indices(delta)
        if indices is not None:
            # print(indices)
            intervals = into_intervals(indices)
            print(intervals)
            # input()
            swipes = create_swipes(
                timestamps,
                word,
                intervals,
                os.path.join(os.getcwd(), "src", "py", "temp", unique_word + ".log"),
            )
            for swipe in swipes:
                print(swipe.stringify())
        elif indices is None:
            warnings.warn("No indices above the threshold, so swipes cannot be made")
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
