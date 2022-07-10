def manhattan(train, test):
    dist = 0
    for index in range(0, len(train)):
        dist += abs(train[index]) - abs(test[index])

    return dist
