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

    @staticmethod
    def time_delta_threshold():
        return int(JSON_Config.get_data()["TIME_DELTA_THRESHOLD"])

    @staticmethod
    def swipe_length_threshold():
        return int(JSON_Config.get_data()["SWIPE_LENGTH_THRESHOLD"])

    @staticmethod
    def adjust_config(threshold_type: Threshold_Type, new_value: int):
        with open(JSON_Config.get_config_path(), "r") as config_file:
            data = json.load(config_file)
            if threshold_type == Threshold_Type.SWIPE_LENGTH:
                data["SWIPE_LENGTH_THRESHOLD"] = new_value
            elif threshold_type == Threshold_Type.TIME_DELTA:
                data["TIME_DELTA_THRESHOLD"] = new_value
        with open(JSON_Config.get_config_path(), "w") as config_file:
            json.dump(data, config_file)


if __name__ == "__main__":
    print(JSON_Config.swipe_length_threshold())
    JSON_Config.adjust_config(Threshold_Type.SWIPE_LENGTH, 40)
    print(JSON_Config.swipe_length_threshold())
