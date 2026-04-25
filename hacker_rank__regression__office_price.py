import numpy as np
# from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# F -> number of features, N -> number tain data, T -> test_size

# For hacker rank -> lines not needed always use input()
# F, N = map(int, input().split())  -> hacker rank

curr_line = 0
with open("input/hacker_rank__regression__office_price.txt", "r") as f:
    lines = f.read().strip().splitlines()
F, N = map(int, lines[curr_line].split())

X_train = []
y_train = []

curr_line = 0

for i in range(N):
    curr_line += 1
    lst = list(map(float, lines[curr_line].split()))
    X_train.append(lst[0:F])
    y_train.append(lst[F])


curr_line += 1
T = int(lines[curr_line])

X_test = []

for i in range(T):
    curr_line += 1
    lst = list(map(float, lines[curr_line].split()))
    X_test.append(lst)

# from list to numpy array
X_train = np.array(X_train)
y_train = np.array(y_train)
X_test = np.array(X_test)


poly = PolynomialFeatures(degree=3)
X_poly_train = poly.fit_transform(X_train)
X_poly_test = poly.fit_transform(X_test)

# modeling
model = LinearRegression()
model.fit(X_poly_train,y_train)

pred = model.predict(X_poly_test)

print(pred)

