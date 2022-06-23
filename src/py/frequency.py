import os
import random
from collections import Counter


def select_files(dir_path: str):
    files = []
    for i in range(0, 10):
        files.append(random.choice(os.listdir(dir_path)))
    return files


def get_word_frequencies(file_list):
    words = []
    # f = select_files(os.path.join(os.getcwd(), "data"))
    for name in file_list:
        file_name = open(os.path.join(os.getcwd(), "data", name), "r")
        lines = file_name.readlines()
        for line in lines:
            word = list(line.split(" "))[10]
            words.append(word)
    # print(words)
    c = Counter(words)
    print(c)


if __name__ == "__main__":
    f = [
        "8k50vo7cakvqthn0v6fdftl1ab.log",
        "5v92ebr64nahqa93mh9t65ofda.log",
        "l1jrsgrnupn8a1938l8l4qhvn3.log",
        "tebbvjq11ah5vujrc0grhuvool.log",
        "ob4mtlqhpto7iin9bjrbmbm8e5.log",
        "64umra5pcbc8n78g2c0ev5c9pg.log",
        "7udhss2800rg0e9k9tqucribhq.log",
        "qge0ctd4dtgqbnorer47fv5cg9.log",
        "ol08ng1j74i3togha376tc8e4m.log",
        "rnfhojlb55ags2q176qd0i7k3n.log",
    ]
get_word_frequencies(f)
