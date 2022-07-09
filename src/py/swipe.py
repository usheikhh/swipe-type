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
        # f = open(self.backing_file.get_path(), "r")
        f = open(self.get_path(), "r")
        lines = f.readlines()
        for line in lines:
            if line.split(" ")[1] == timestamp:
                return line


class Swipe:
    def __init__(self, key: str, backing_file: Backing_File, swipe_data):
        self.key = key
        self.backing_file = backing_file
        self.swipe_data = swipe_data

    def get_key(self):
        return self.key

    def x_pos(self, timestamp: str):
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[5]

    def y_pos(self, timestamp: str):
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[6]

    def sentence(self, timestamp: str):
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[0]

    def first_and_last_timestamp(self):
        return [self.swipe_data[0], self.swipe_data[-1]]

    def last_timestamp(self):
        return self.swipe_data[-1]

    def first_timestamp(self):
        return self.swipe_data[0]

    def event(self, timestamp: str):
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[4]

    def x_radius(self, timestamp: str):
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[7]

    def y_radius(self, timestamp: str):
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[8]

    def get_word(self, timestamp: str):
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[10]

    def swipe_timestamps(self):
        return self.swipe_data

    def timestamp_at(self, index: int):
        return self.swipe_timestamps[index]

    def stringify(self):
        return f"Word: {self.key} Timestamps {self.swipe_data}"

    def get_backing_file(self) -> Backing_File:
        return self.backing_file
