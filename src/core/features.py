from core.swipe import Swipe
from math import floor
from core.log import Logger

# This function creates an array of the length of from point to point
def pairwise_length_vector(swipe: Swipe):
    length_vector = []
    times = swipe.swipe_timestamps()
    # print("Times: ", times)
    x_coords = []
    y_coords = []
    for time in times:
        x_coords.append(int(swipe.x_pos(time)))
        y_coords.append(int(swipe.y_pos(time)))
    # print("X positions: ", (x_coords))
    # print("Y positions: ", (y_coords))
    for i in range(0, len(x_coords) - 1):
        x1 = x_coords[i]
        x2 = x_coords[i + 1]
        y1 = y_coords[i]
        y2 = y_coords[i + 1]
        length_vector.append(pow(pow((y2 - y1), 2) + pow((x2 - x1), 2), 0.5))
    return length_vector


def straight_line_distance(swipe: Swipe):
    times = swipe.first_and_last_timestamp()
    assert len(times) == 2
    first_timestamp = times[0]
    last_timestamp = times[1]
    x1 = int(swipe.x_pos(first_timestamp))
    x2 = int(swipe.x_pos(last_timestamp))
    y1 = int(swipe.y_pos(first_timestamp))
    y2 = int(swipe.y_pos(last_timestamp))
    # TODO: Find better ways to handle division by zero errors
    try:
        return float((y2 - y1) / (x2 - x1))
    except ZeroDivisionError:
        log = Logger()
        log.km_error("Divide by zero error when calculating straight line distance")
        return 0


def pairwise_velocity_vector(swipe: Swipe):
    length_vector = pairwise_length_vector(swipe)
    delta_vector = Feature_Extractor.time_delta(swipe)
    # print(len(length_vector), len(delta_vector))
    try:
        assert len(length_vector) == len(
            delta_vector
        ), "Pairwise length and pairwise delta vectors are not the same length"
    except AssertionError:
        if len(length_vector) > len(delta_vector):
            while len(length_vector) > len(delta_vector):
                length_vector.pop()
        elif len(length_vector) < len(delta_vector):
            while len(length_vector) < len(delta_vector):
                delta_vector.pop()
    velocities = []
    for i in range(0, len(length_vector)):
        velocities.append(float(length_vector[i]) / int(delta_vector[i]))
    return velocities


def pairwise_acceleration_vector(swipe: Swipe):
    acceleration_vector = []
    velocity_vector = pairwise_velocity_vector(swipe)
    time_delta_vector = Feature_Extractor.time_delta(swipe)
    assert len(velocity_vector) == len(
        time_delta_vector
    ), "Velocities and time deltas should be the same length"

    for i in range(0, len(velocity_vector)):
        acceleration_vector.append(float(velocity_vector[i]) / time_delta_vector[i])
    return acceleration_vector


class Feature_Extractor:
    def __init__(self):
        pass

    @staticmethod
    def length(swipe: Swipe):
        #! FIXME: We need to figure out which file is giving us a divide by zero error and why
        pairwise_lengths = pairwise_length_vector(swipe)
        return sum(pairwise_lengths)

    @staticmethod
    def time_delta(swipe: Swipe):
        timestamps = swipe.swipe_timestamps()
        try:
            # print(timestamps)
            curr = int(timestamps[0])
            # print("curr", curr)
            deltas = []
            for i in range(1, len(timestamps)):
                delta = int(timestamps[i]) - curr
                if delta > 0:
                    deltas.append(delta)
                curr = int(timestamps[i])
            return deltas
        except ValueError:
            # print(timestamps)
            curr = int(timestamps[1])
            print("curr", curr)
            deltas = []
            for i in range(2, len(timestamps)):
                delta = int(timestamps[i]) - curr
                deltas.append(delta)
                curr = int(timestamps[i])
            return deltas

    @staticmethod
    def calculate_velocity(swipe: Swipe):
        return sum(pairwise_velocity_vector(swipe))

    @staticmethod
    def calculate_average_velocity(swipe: Swipe):
        return float(
            sum(pairwise_velocity_vector(swipe)) / len(pairwise_velocity_vector(swipe))
        )

    @staticmethod
    def calculate_pairwise_acceleration(swipe: Swipe):
        return sum(pairwise_acceleration_vector(swipe))

    @staticmethod
    def percentile_velocity(initial_swipe: Swipe, percentile: float = 0.2):
        if percentile >= 1.0 or percentile <= 0.0:
            raise ValueError("Percentile should be between 0 and 1 non-inclusive")
        velocity_vector = pairwise_velocity_vector(initial_swipe)
        row_count = floor(len(velocity_vector) * percentile)
        return sum(velocity_vector[0:row_count])

    @staticmethod
    def deviation_ratio(swipe: Swipe):
        try:
            return float(
                Feature_Extractor.length(swipe) / abs(straight_line_distance(swipe))
            )
        except ZeroDivisionError:
            log = Logger()
            log.km_error("Divide by zero error when calculating deviation ratio")
            return 0

    @staticmethod
    def extract_all_features(swipe: Swipe):
        feature_values = {}
        feature_values["length"] = Feature_Extractor.length(swipe)
        feature_values["Velocity"] = Feature_Extractor.calculate_velocity(swipe)
        feature_values[
            "Pairwise acceleration"
        ] = Feature_Extractor.calculate_pairwise_acceleration(swipe)
        feature_values["Percentile Velocity"] = Feature_Extractor.percentile_velocity(
            swipe
        )
        feature_values["Deviation Ratio"] = Feature_Extractor.deviation_ratio(swipe)
        return feature_values

    @staticmethod
    def extract_all_features_to_list(swipe: Swipe):
        features = Feature_Extractor.extract_all_features(swipe)
        return list(features.values())
