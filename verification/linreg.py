# from https://www.w3schools.com/python/python_ml_linear_regression.asp

import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

# Data
x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

# Perform linear regression
slope, intercept, r, p, std_err = stats.linregress(x, y)

# Define regression function
def myfunc(x):
  return slope * x + intercept

# Model predictions
mymodel = list(map(myfunc, x))

# Calculate R^2, MAE, MSE, and RMSE
r_squared = r**2
mae = mean_absolute_error(y, mymodel)
mse = mean_squared_error(y, mymodel)
rmse = np.sqrt(mse)

# Print stats
print(f"Slope: {round(slope,2)}, Intercept: {round(intercept,2)}")
print(f"R: {round(r,2)}, R^2: {round(r_squared,2)}")
print(f"P-value: {round(p,5)}, Standard Error: {round(std_err,2)}")
print(f"MAE: {round(mae,2)}, MSE: {round(mse,2)}, RMSE: {round(rmse,2)}")

# Plot
plt.scatter(x, y, label='Data points')
plt.plot(x, mymodel, color='orange', label='Regression line')
plt.legend()
plt.show()
