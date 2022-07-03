def string_to_list(string: str):
    # FIXME: Improve this regex so it only looks at spaces and does not accidentally think a quote, or anything else, is
    # part of the expression string
    res = list(string.split(" "))
    return res


class Backing_File:
    def __init__(self, path: str):
        self.path = path

    def get_path(self):
        return self.path

    def lookup_row_by_timestamp(self, timestamp: str):
        f = open(self.backing_file.get_path(), "r")
        lines = f.readlines()
        for line in lines:
            if line.split(" ")[1] == timestamp:
                return line


class Swipe:
    def __init__(self, key, backing_file, swipe_data):
        self.key = key
        self.backing_file = backing_file
        self.swipe_data = swipe_data

    def get_key(self):
        return self.key

    def x_pos(self):
        pass

    def y_pos(self):
        pass

    def sentence(self):
        pass

    def first_and_last_timestamp(self):
        pass

    def event(self):
        pass

    def x_radius(self):
        pass

    def y_radius(self):
        pass

    def get_word(self):
        pass

    def swipe_timestamps(self):
        return self.swipe_data

    def stringify(self):
        return f"Word: {self.key} Timestamps {self.swipe_data}"

    def get_backing_file(self):
        return self.backing_file
