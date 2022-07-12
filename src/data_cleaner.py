import os
import json


def get_all_json_files(dir_path: str, keep_android: bool = True):
    root_path = os.path.join(os.getcwd(), dir_path)
    for file in os.listdir(root_path):
        if file.endswith(".json"):
            final_path = os.path.join(root_path, file)
            if check_vendor(final_path) == "Apple Computer, Inc." and keep_android:
                file_name = os.path.splitext(file)[0]
                print(os.path.join(root_path, file_name + ".log"))
                if os.path.exists(os.path.join(root_path, file_name + ".log")):
                    os.remove(os.path.join(root_path, file_name + ".log"))
                    delete_json_files(dir_path)


def check_vendor(path: str):
    f = open(path, "r")
    data = json.load(f)
    print(data["vendor"])
    return data["vendor"]


def delete_json_files(dir_path: str):
    root_path = os.path.join(os.getcwd(), dir_path)
    for file in os.listdir(root_path):
        if file.endswith(".json"):
            file_name = os.path.splitext(file)[0]
            os.remove(os.path.join(root_path, file_name + ".json"))


if __name__ == "__main__":
    get_all_json_files("data/")
