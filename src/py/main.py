from swipe_extractor import (
    compute_timestamp_deltas,
    extract_timestamps,
    extract_swipes_indices,
    into_intervals,
    create_swipes,
)
from swipe_extractor import grab_first
import os


if __name__ == "__main__":
    timestamps, word = extract_timestamps(
        os.path.join(os.getcwd(), "src", "py", "delay.log")
    )
    print(word)
    delta = compute_timestamp_deltas(timestamps)
    indices = extract_swipes_indices(delta)
    intervals = into_intervals(indices)
    swipes = create_swipes(timestamps, word, intervals)
    for swipe in swipes:
        print(swipe.stringify())
