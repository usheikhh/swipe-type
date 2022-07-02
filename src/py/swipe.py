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

    def swipe_timestamps(self):
        return self.swipe_data

    def stringify(self):
        return f"Word: {self.key} Timestamps {self.swipe_data}"
