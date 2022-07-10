from swipe import Swipe


class Feature_Extractor:
    def __init__(self):
        pass

    @staticmethod
    def length(swipe: Swipe):
        #! FIXME: We need to figure out which file is giving us a divide by zero error and why
        first_timestamp, last_timestamp = swipe.first_and_last_timestamp()
        x1 = swipe.x_pos(first_timestamp)
        y1 = swipe.y_pos(first_timestamp)
        x2 = swipe.x_pos(last_timestamp)
        y2 = swipe.y_pos(last_timestamp)
        print("X1: ", x1, "Y1: ", y1, "X2: ", x2, "Y2: ", y2)
        try:
            return float(abs(int(y2) - int(y1)) / abs(int(x2) - int(x1)))
        except ZeroDivisionError:
            # print("Calculating swipe length")
            print("Key:", swipe.get_key())
            # print("Path:", swipe.get_backing_file().get_path())
            return 0

    @staticmethod
    def length_between_swipes(initial_swipe: Swipe, other_swipe: Swipe):
        # XXX: Condense: employ a similar approach to length() with only a single swipe... remember that the returned row is one giant string not a list of smaller strings
        first_timestamp = initial_swipe.first_timestamp()
        ending_timestamp = other_swipe.last_timestamp()
        first_row = initial_swipe.get_backing_file().lookup_row_by_timestamp(
            first_timestamp
        )

        second_row = other_swipe.get_backing_file().lookup_row_by_timestamp(
            ending_timestamp
        )

        x1 = int(first_row[5])
        y1 = int(first_row[6])
        x2 = int(second_row[5])
        y2 = int(second_row[6])
        return float((y2 - y1) / (x2 - x1))

    @staticmethod
    def time_delta_between_swipes(swipe: Swipe, other_swipe: Swipe):
        return int(swipe.first_timestamp()) - int(other_swipe.second_timestamp())

    @staticmethod
    def velocity_between_swipes(initial_swipe: Swipe, other: Swipe):
        # TODO: I think this is right, not sure though
        displacement = Feature_Extractor.length_between_swipes(initial_swipe, other)
        delta_t = Feature_Extractor.time_delta_between_swipes(initial_swipe, other)
        return float(displacement / delta_t)

    @staticmethod
    def acceleration_between_swipes(initial_swipe: Swipe, other: Swipe):
        velocity = Feature_Extractor.calculate_velocity(initial_swipe, other)
        time = Feature_Extractor.time_delta(initial_swipe, other)
        return float(velocity / time)

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
