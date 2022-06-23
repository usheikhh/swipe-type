import pandas as pd
import os

from swipe import Swipe, SwipeSet


def grab_first():
    path = os.path.join(os.getcwd(), "data")
    first = os.listdir(path)[0]
    print(first)
    pd.options.display.max_columns = None
    df = pd.read_csv(os.path.join(path, first))
    return df


def unique_words(df: pd.DataFrame):
    data = df.iloc[:, :1].values.tolist()
    store = []
    for row in data:
        # Since the log file is not actually a csv we can't do a simple column name/index lookup
        string = row[10]
        sep = " "
        # Use a regex of the space character to split out the sentence column from the string
        sentence = string.split(sep, 1)[0]
        store.append(sentence)
    return set(store)


def unique_sentences(df: pd.DataFrame):
    data = df.iloc[:, :1].values.tolist()
    store = []
    for row in data:
        # Since the log file is not actually a csv we can;t do a simple column name/index lookup
        string = row[0]
        sep = " "
        # Use a regex of the space character to split out the sentence column from the string
        sentence = string.split(sep, 1)[0]
        store.append(sentence)
    return set(store)


def into_swipe_set(df: pd.DataFrame):
    data = df.iloc[:, :1].values.tolist()
    unique = unique_sentences(df)
    store = []
    for sentence in unique:
        for row in data:
            string = row[0]
            sep = " "
            found = string.split(sep, 1)[0]
            remaining = str(string.split(sep, 1)[1:])
            if found == sentence:
                store.append(Swipe(sentence, remaining))
    return store
