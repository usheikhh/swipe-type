class Backing_File:
    # The Backing_File is a data structure representing a word-level log file that backs up swipe(s) for that word
    # So the Backing_File contains all of the touchpoint information for all the swipes that we can programmatically
    # generate for a word.
    # Each individual touchpoint contains information about its respective:
    #   - x_pos
    #   - y_pos
    #   - timestamp
    #   - x_radius
    #   - y_radius
    #   - swiped word
    def __init__(self, path: str):
        self.path = path

    def get_path(self):
        return self.path

    def lookup_row_by_timestamp(self, timestamp: str):
        # By knowing all the timestamps of all the touchpoints that make up a swipe of a word we can
        # extract the other previously mentioned metadata associated with it
        f = open(self.get_path(), "r", encoding="UTF-8")
        lines = f.readlines()
        for line in lines:
            if line.split(" ")[1] == timestamp:
                return line


class Swipe:
    # A swipe is a data structure representing a user makes when swipe-typing a word.
    # key: the word being swiped
    # backing_file: the word-level log file with all the touchpoints that make up the word.
    # From these touchpoints, the swipes can be generated
    # swipe_data: The list of timestamps that make up the swipe
    def __init__(self, key: str, backing_file: Backing_File, swipe_data):
        self.key = key
        self.backing_file = backing_file
        self.swipe_data = swipe_data

    def get_key(self):
        return self.key

    def x_pos(self, timestamp: str):
        # Get the x position of a touchpoint at a given timestamp
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        # FIX: I dont know if this is a bug with
        # how we are sending the swipe data to the swipe object or if we accidentally
        # shave off a row somewhere but i looks like when printing out the rows in the file
        # the last row is missing, or at least it is for delay.log
        # print("Found row:", row)
        return row[5]

    def y_pos(self, timestamp: str):
        # Get the y position of a touchpoint at a given timestamp
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        # print("Found row:", row)
        return row[6]

    def sentence(self, timestamp: str):
        # Get the sentence of a touchpoint at a given timestamp
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[0]

    def first_and_last_timestamp(self):
        # Get the first and last timestamp of a swipe
        return [self.swipe_data[0], self.swipe_data[-1]]

    def last_timestamp(self):
        # Get the last timestamp of a swipe
        return self.swipe_data[-1]

    def first_timestamp(self):
        # Get the first timestamp of a swipe
        return self.swipe_data[0]

    def event(self, timestamp: str):
        # Get the touchpoint event at a given timestamp. There are 3 possible event types:
        # 1) Touchstart: the touch point starting a swipe
        # 2) Touchmove: the touch point gwhile the swipe is being generated
        # 3) Touchend: the last touch point making up the swipe
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[4]

    def x_radius(self, timestamp: str):
        # Get the x radius of a touchpoint at a given timestamp
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[7]

    def y_radius(self, timestamp: str):
        # Get the y radius of a touchpoint at a given timestamp
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[8]

    def get_word(self, timestamp: str):
        # Get the word being swiped at a given timestamp
        row = self.get_backing_file().lookup_row_by_timestamp(timestamp)
        row = row.split(" ")
        return row[10]

    def swipe_timestamps(self):
        # Get all the timestamps that make up the swipe
        # print(self.swipe_data)
        # print("Found", len(self.swipe_data), "timestamps")
        return self.swipe_data

    def timestamp_at(self, index: int):
        # Get the timestamp at a particular index
        return self.swipe_timestamps[index]

    def stringify(self):
        # Stringify a swipe for debugging
        return f"Word: {self.key} Timestamps {self.swipe_data}"

    def get_backing_file(self) -> Backing_File:
        # Get the backing_file associated with a swipe
        return self.backing_file
