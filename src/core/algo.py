from scipy.spatial.distance import cityblock
from math import sqrt
import numpy as np
from features import Feature_Extractor
import matplotlib.pyplot as plt


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
            false_reject += 1
    return false_reject / total_genuine_scores


def calc_FAR(threshold, impostor_scores: list):
    false_accept = 0
    total_impostor_scores = len(impostor_scores)
    for score in impostor_scores:
        if score <= threshold:
            false_accept += 1
    return false_accept / total_impostor_scores


def calc_EER(threshold, genuine_scores, impostor_scores):
    return (
        calc_FAR(threshold, impostor_scores) + calc_FRR(threshold, genuine_scores)
    ) / 2


def DET_curve(
    min_threshold: int,
    max_threshold: int,
    genuine_scores: list,
    impostor_scores: list,
    step: float = 1.0,
):
    i = min_threshold
    FRR_values = []
    FAR_values = []
    for i in np.arange(min_threshold, max_threshold, step):
        FRR_values.append(calc_FRR(i, genuine_scores))
        FAR_values.append(calc_FAR(i, impostor_scores))
    t = np.linspace(min_threshold, max_threshold, 8000)
    plt.plot(t, FAR_values, label="FAR Values")
    plt.plot(t, FRR_values, label="FRR Values")
    plt.legend()
    plt.savefig("DET.png")
    plt.show()
