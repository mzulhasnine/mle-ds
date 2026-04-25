'''
Problem 1: Train/Test Split from Scratch
Implement:

def train_test_split(X, y, test_size=0.2, random_state=42):
    pass

Requirements:

X is a list of rows
y is a list of labels
shuffle data using random_state
return X_train, X_test, y_train, y_test
Example:

X = [[1], [2], [3], [4], [5]]
y = [0, 0, 1, 1, 1]

Expected:

80% train
20% test
shuffled before split


'''

import random

def train_test_split(X, y, test_size=0.2, random_state=42):

    n = len(X)

    indices = list(range(n))

    random.seed(random_state)
    random.shuffle(indices)
    
    n_test_size = int(n*test_size)
    n_train_size = n - n_test_size


    indices_train = indices[:n_train_size]
    indices_test = indices[n_train_size:]


    X_train = [X[i] for i in indices_train]
    X_test = [X[i] for i in indices_test]

    y_train = [y[i] for i in indices_train]
    y_test = [y[i] for i in indices_test]


    return X_train, X_test, y_train, y_test


if __name__ == "__main__":


    # Problem 1: Train/Test Split from Scratch
    X = [[1], [2], [3], [4], [5]]
    y = [0, 0, 1, 1, 1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(X_train, y_train)
    print(X_test,y_test)
