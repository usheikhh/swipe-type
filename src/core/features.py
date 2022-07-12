from cmath import sqrt
from swipe import Swipe
import numpy as np


def split_into_sized_chunks(lst, size: int):
    return np.array_split(lst, size)


class Feature_Extractor:
    def __init__(self):
        pass

    @staticmethod
    def length(swipe: Swipe):
        #! FIXME: We need to figure out which file is giving us a divide by zero error and why
        times = swipe.swipe_timestamps()
        print("Times: ", times)
        x_coords = []
        y_coords = []
        for time in times:
            x_coords.append(int(swipe.x_pos(time)))
            y_coords.append(int(swipe.y_pos(time)))
        # print("X positions: ", (x_coords))
        # print("Y positions: ", (y_coords))
        sum = 0
        for i in range(0, len(x_coords) - 1):
            x1 = x_coords[i]
            x2 = x_coords[i + 1]
            y1 = y_coords[i]
            y2 = y_coords[i + 1]
            sum += (pow(pow((y2-y1),2) + pow((x2-x1),2),0.5))
        return sum

    @staticmethod
    def time_delta(initial_swipe: Swipe):
        first_timestamp, last_timestamp = initial_swipe.first_and_last_timestamp()
        return int(last_timestamp) - int(first_timestamp)

    @staticmethod
    def calculate_velocity(swipe: Swipe):
        times = swipe.swipe_timestamps()
        print("Times: ", times)
        x_coords = []
        y_coords = []
        for time in times:
            x_coords.append(int(swipe.x_pos(time)))
            y_coords.append(int(swipe.y_pos(time)))
        pairwise_velocities = []
        for i in range(len(x_coords) - 2):
            x1 = x_coords[i]
            x2 = x_coords[i + 1]
            y1 = y_coords[i]
            y2 = y_coords[i + 1]
            t1 = int(times[i])
            t2 = int(times[i + 1])
            delta_y = y2 - y1
            delta_x = x2 - x1
            delta_t = t2 - t1
            pairwise_velocities.append(float(delta_y / delta_x / delta_t))
        return pairwise_velocities

    @staticmethod
    def calculate_acceleration(initial_swipe: Swipe):
        velocity = Feature_Extractor.calculate_velocity(initial_swipe)
        time = Feature_Extractor.time_delta(initial_swipe)

        return float(velocity / time)

    @staticmethod
    def percentile_velocity(initial_swipe: Swipe, percentile: float):
        if percentile >= 1.0 or percentile <= 0.0:
            raise ValueError("Percentile should be between 0 and 1 non-inclusive")
        velocity = Feature_Extractor.calculate_velocity(initial_swipe)
        return float(velocity * percentile)

    @staticmethod
    def extract_all_features(swipe: Swipe):
        feature_values = {}
        feature_values["length"] = Feature_Extractor.length(swipe)
        feature_values["velocity"] = Feature_Extractor.calculate_velocity(swipe)
        feature_values["acceleration"] = Feature_Extractor.calculate_acceleration(swipe)
        feature_values["percentile"] = Feature_Extractor.percentile_velocity(swipe, 0.3)
        return feature_values
