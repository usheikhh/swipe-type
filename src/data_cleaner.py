import os
import json
from core.swipe_extractor import (
    extract_trajectories,
    unique_words_from_file,
    write_to_file,
)
from tqdm import tqdm


def generate_word_files():
    p = os.path.join(os.getcwd(), "data")
    onlyfiles = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    for file in tqdm(onlyfiles):
        # print(file)
        words = unique_words_from_file(os.path.join(os.getcwd(), "data", file))
        # print(words)
        for unique_word in words:
            # At this current moment we can reasonably assume that all the files have been generated
            trajectories, word = extract_trajectories(
                os.path.join(os.getcwd(), "data", file),
                unique_word,
            )
            write_to_file(trajectories, unique_word)


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
    try:
        get_all_json_files("data/")
    except FileNotFoundError:
        pass
    try:
        generate_word_files()
    except UnicodeDecodeError:
        pass
