# from https://www.w3schools.com/python/python_ml_linear_regression.asp

import matplotlib.pyplot as plt
from scipy import stats

x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

print(f"Slope: {round(slope,2)}, Intercept: {round(intercept,2)}, R: {round(r,2)}, P: {round(p,5)}, Standard Error: {round(std_err,2)}")

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()