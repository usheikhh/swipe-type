from scipy.spatial.distance import cityblock
from math import sqrt

from features import Feature_Extractor


def manhattan(train, test):
    dist = 0
    for index in range(0, len(train)):
        dist += abs(train[index]) - abs(test[index])

    return dist


def scipy_manhattan(train, test):
    return cityblock(train, test)


def euclidean_distance(a, b):
    return sqrt(sum((e1 - e2) ** 2 for e1, e2 in zip(a, b)))


def score_calc(template, impostor_swipe):
    return scipy_manhattan(
        template, Feature_Extractor.extract_all_features_to_list(impostor_swipe)
    )

def calc_FRR(threshold, genuine_scores: list):
    false_reject = 0
    total_genuine_scores = len(genuine_scores)
    for score in genuine_scores:
        if score > threshold:
            false_reject+=1
    return false_reject/total_genuine_scores

def calc_FAR(threshold, impostor_scores: list):
    false_accept = 0
    total_impostor_scores = len(impostor_scores)
    for score in impostor_scores:
        if score <= threshold:
            false_accept +=1
    return false_accept/total_impostor_scores
