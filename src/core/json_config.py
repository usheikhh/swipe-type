import json
import enum
import os


class Threshold_Type(enum.Enum):
    SWIPE_LENGTH = 0
    TIME_DELTA = 1


class JSON_Config:
    config_path = os.path.join(os.getcwd(), "config.json")

    def __init__(self):
        pass

    @staticmethod
    def get_config_path():
        return JSON_Config.config_path

    @staticmethod
    def set_config_path(new_config_path: str):
        JSON_Config.config_path = new_config_path

    @staticmethod
    def get_data():
        with open(JSON_Config.get_config_path()) as config_file:
            data = json.load(config_file)
        return data

    def time_delta_threshold():
        return int(JSON_Config.get_data()["TIME_DELTA_THRESHOLD"])

    def swipe_length_threshold():
        return int(JSON_Config.get_data()["SWIPE_LENGTH_THRESHOLD"])


if __name__ == "__main__":
    print(JSON_Config.swipe_length_threshold())
