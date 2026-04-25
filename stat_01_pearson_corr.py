import numpy as np
import math

X = [15.0, 12.0, 8.0, 8.0, 7.0, 7.0, 7.0, 6.0, 5.0, 3.0]
Y = [10.0, 25.0, 17.0, 11.0, 13.0, 17.0, 20.0, 13.0, 9.0, 15.0]

numerator = 0

x_avg = np.mean(X)
y_avg = np.mean(Y)

sum_dx_sq = 0 
sum_dy_sq = 0 

for i in range(len(X)):
    dx = X[i] - x_avg
    dy = Y[i] - y_avg
    
    numerator += dx*dy
    sum_dx_sq += dx**2 
    sum_dy_sq += dy**2 

denomirator = math.sqrt(sum_dx_sq*sum_dy_sq)

pearson_corr = numerator/denomirator

print(pearson_corr)