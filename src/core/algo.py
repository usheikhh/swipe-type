from scipy.spatial.distance import cityblock
from math import sqrt
import numpy as np
from core.features import Feature_Extractor
import matplotlib.pyplot as plt


def manhattan(train, test):
    """Manually calculate the manhattan distance between feature arrays
    This method was really only a test and should not be used and will be removed eventually
    """
    dist = 0
    for index in range(0, len(train)):
        dist += abs(train[index]) - abs(test[index])

    return dist


def scipy_manhattan(train, test):
    """Calculate the manhattan distance between feature arrays"""
    return cityblock(train, test)


def euclidean_distance(a, b):
    """Calculate the Euclidean distance between feature arrays"""
    return sqrt(sum((e1 - e2) ** 2 for e1, e2 in zip(a, b)))


def score_calc(template, impostor_swipe):
    """Calculate the manhattan distance between the genuine and impostor vectors"""
    return scipy_manhattan(
        template, Feature_Extractor.extract_all_features_to_list(impostor_swipe)
    )


def calc_FRR(threshold, genuine_scores: list):
    # XXX: Double Check
    """Return a float percentage of the False Rejection Ratio or the number of scores that are above a specified threshold"""
    false_reject = 0
    total_genuine_scores = len(genuine_scores)
    for score in genuine_scores:
        if score > threshold:
            false_reject += 1
    return false_reject / total_genuine_scores


def calc_FAR(threshold, impostor_scores: list):
    # XXX: Double Check
    """Return a float percentage of the False Acceptance Ratio or the number of impostor scores that are below a specified threshold"""
    false_accept = 0
    total_impostor_scores = len(impostor_scores)
    for score in impostor_scores:
        if score <= threshold:
            false_accept += 1
    return false_accept / total_impostor_scores


def calc_EER(threshold, genuine_scores, impostor_scores):
    """The EER is calculated by averaging the FAR and FRR"""
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
    """Create a running plot of the FAR and FRR values given a specific threshold as determined by our data"""
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
    # plt.suptitle("Length Feature FAR vs FRR curve")
    plt.xlabel("Threshold", fontsize=18)
    plt.ylabel("Percentage", fontsize=16)

    plt.savefig("DET.png")
    plt.show()
