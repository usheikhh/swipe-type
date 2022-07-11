from turtle import distance
from scipy.spatial.distance import cityblock
from math import sqrt


def manhattan(train, test):
    dist = 0
    for index in range(0, len(train)):
        dist += abs(train[index]) - abs(test[index])

    return dist


def scipy_manhattan(train, test):
    return cityblock(train, test)


def euclidean_distance(a, b):
    return sqrt(sum((e1 - e2) ** 2 for e1, e2 in zip(a, b)))
