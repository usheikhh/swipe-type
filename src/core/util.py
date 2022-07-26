import pickle


def flatten(xss):
    return [x for xs in xss for x in xs]


def loadall(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break
