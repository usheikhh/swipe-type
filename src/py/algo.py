import numpy as np


def manhattan(train, test):

    dist = []
    train = train.to_numpy()
    for ind, r in test.iterrows():
        r = r.to_numpy()
        distance = np.abs(train - r).sum(-1)

        idx = np.argpartition(distance, 10)
        dist.append(idx[:10])

    return dist
