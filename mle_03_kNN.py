import math
from collections import Counter


def euclidean_distance(a, b):
    # distance = sqrt(sum of squared differences across all features) >> sqrt ( sum  (x_i - y_i)**2 )
    # total = 0
    # for i in range(len(a)):
    #     total += (a[i] - b[i])**2

    total = sum((x-y)**2 for x,y in zip(a,b))

    return math.sqrt(total)


class KNNClassifier:

    def __init__(self, k=3):
        self.k = k
        self.X_train = []
        self.y_train = []

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict_one(self, x):

        distances = []

        for i in range(len(self.X_train)):
            dist = euclidean_distance(x, self.X_train[i])
            distances.append((dist, self.y_train[i]))

        distances.sort(key=lambda x: x[0])

        k_nearest = distances[0:self.k]

        freq = Counter([e[1] for e in k_nearest])

        count = -1
        for k,v in freq.items():
            if v>count: 
                most_common = k 

        return most_common


    def predict(self, X):
        return [self.predict_one(x) for x in X]


if __name__ == "__main__":
    X_train = [
        [1, 2],
        [2, 3],
        [3, 3],
        [6, 5],
        [7, 7],
        [8, 6],
    ]

    y_train = [0, 0, 0, 1, 1, 1]

    X_test = [
        [2, 2],
        [7, 6],
    ]

    model = KNNClassifier(k=3)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print(preds)  # [0, 1]