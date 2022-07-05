from swipe import Swipe


class Feature_Extractor:
    @staticmethod
    def length(swipe: Swipe):
        # XXX: Condense
        first_timestamp, last_timestamp = swipe.first_and_last_timestamp()
        first_row = swipe.get_backing_file().lookup_row_by_timestamp(first_timestamp)
        second_row = swipe.get_backing_file().lookup_row_by_timestamp(last_timestamp)
        x1 = first_row[5]
        y1 = first_row[6]
        x2 = second_row[5]
        y2 = second_row[6]
        return float((y2 - y1) / (x2 - x1))

    @staticmethod
    def length_between_swipes(initial_swipe: Swipe, other_swipe: Swipe):
        # XXX: Condense
        first_timestamp = initial_swipe.first_timestamp()
        ending_timestamp = other_swipe.last_timestamp()
        first_row = initial_swipe.get_backing_file().lookup_row_by_timestamp(
            first_timestamp
        )

        second_row = other_swipe.get_backing_file().lookup_row_by_timestamp(
            ending_timestamp
        )

        x1 = first_row[5]
        y1 = first_row[6]
        x2 = second_row[5]
        y2 = second_row[6]
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
        displacement = Feature_Extractor.length(swipe)
        delta_t = Feature_Extractor.time_delta(swipe)
        return float(displacement / delta_t)

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
