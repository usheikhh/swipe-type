from scipy.stats import linregress
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
        return linregress(x_coords, y_coords).slope

    @staticmethod
    def time_delta_between_swipes(swipe: Swipe, other_swipe: Swipe):
        pass

    @staticmethod
    def velocity_between_swipes(initial_swipe: Swipe, other: Swipe):
        pass

    @staticmethod
    def acceleration_between_swipes(initial_swipe: Swipe, other: Swipe):
        pass

    @staticmethod
    def time_delta(initial_swipe: Swipe):
        first_timestamp, last_timestamp = initial_swipe.first_and_last_timestamp()
        return int(last_timestamp) - int(first_timestamp)

    @staticmethod
    def calculate_velocity(swipe: Swipe):
        # TODO: I think this is right, not sure though
        # FIXME: There is a divide by zero here
        displacement = Feature_Extractor.length(swipe)
        delta_t = Feature_Extractor.time_delta(swipe)
        try:
            return float(displacement / delta_t)
        except ZeroDivisionError:
            print("Calculating swipe velocity")
            print("Key:", swipe.get_key())
            print("Path:", swipe.get_backing_file().get_path())
            return 0

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
