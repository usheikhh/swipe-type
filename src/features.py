from swipe import Swipe


def time_delta(initial_swipe: Swipe, end_swipe: Swipe):
    return int(end_swipe.timestamp()) - int(initial_swipe.timestamp())


def calculate_velocity(initial_swipe: Swipe, end_swipe: Swipe):
    y_delta = int(end_swipe.y_pos()) - int(initial_swipe.y_pos())
    x_delta = int(end_swipe.x_pos()) - int(initial_swipe.x_pos())
    slope = float(y_delta / x_delta)
    delta_time = time_delta(initial_swipe, end_swipe)
    return float(slope / delta_time)


def calculate_acceleration(initial_swipe: Swipe, end_swipe: Swipe):
    velocity = calculate_velocity(initial_swipe, end_swipe)
    time = time_delta(initial_swipe, end_swipe)
    return float(velocity / time)


def percentile_velocity(initial_swipe: Swipe, end_swipe, percentile: float):
    if percentile >= 1.0 or percentile <= 0.0:
        raise ValueError("Percentile should be between 0 and 1 non-inclusive")
    velocity = calculate_velocity(initial_swipe, end_swipe)
    return float(velocity * percentile)


def calculate_slope(initial_swipe: Swipe, end_swipe):
    y_delta = int(end_swipe.y_pos()) - int(initial_swipe.y_pos())
    x_delta = int(end_swipe.x_pos()) - int(initial_swipe.x_pos())
    slope = float(y_delta / x_delta)
    return slope
