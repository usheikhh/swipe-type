from typing import List


def string_to_list(string: str):
    # FIXME: Improve this regex so it only looks at spaces and does not accidentally think a quote, or anything else, is
    # part of the expression string
    res = list(string.split(" "))
    return res


class Swipe:
    def __init__(self, key, swipe_data):
        self.key = key
        self.swipe_data = swipe_data

    def get_key(self):
        return self.key

    def get_swipe_data(self):
        swipe_data_list = string_to_list(self.swipe_data)
        return swipe_data_list

    def timestamp(self):
        return self.get_swipe_data()[0]

    def keyboard_width(self):
        return self.get_swipe_data()[1]

    def keyboard_height(self):
        return self.get_swipe_data()[2]

    def event(self):
        return self.get_swipe_data()[3]

    def x_pos(self):
        return self.get_swipe_data()[4]

    def y_pos(self):
        return self.get_swipe_data()[5]

    def x_radius(self):
        return self.get_swipe_data()[6]

    def y_radius(self):
        return self.get_swipe_data()[7]

    def angle(self):
        return self.get_swipe_data()[8]

    def word(self):
        return self.get_swipe_data()[9]

    def is_error(self):
        return self.get_swipe_data()[10]

    def stringify(self):
        return f"Key: {self.key}, Timestamp: {self.timestamp()}, Keyboard Width: {self.keyboard_width()}, Keyboard Height: {self.keyboard_height()}, Swipe Event: {self.event()}, X Position: {self.x_pos()}, Y Position: {self.y_pos()}, X Radius: {self.x_radius()}, Y Radius: {self.y_radius()}, Angle: {self.angle()}, Word: {self.word()}, Is an Error: {self.is_error()}"

    def __str__(self):
        return self.stringify()


class SwipeSet:
    def __init__(self, swipe_list: List[Swipe]):
        self.swipe_list = swipe_list

    def get_swipe_list(self):
        return self.swipe_list

    def stringify(self):
        for swipe in self.swipe_list:
            print(swipe.stringify())
