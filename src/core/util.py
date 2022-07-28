import pickle


def flatten(xss):
    """Given a list with 1 or more arrays of arrays, flatten them to a single array"""
    return [x for xs in xss for x in xs]


def loadall(filepath):
    """Load a pickle file by passing in its absolute file path"""
    with open(filepath, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break
