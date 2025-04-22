import math
import matplotlib.pyplot as plt
import csv
from scipy import stats

# profile data
max_v = 26.8 # velocity (m/s)
max_a = max_v/3 # acceleration (m/s^2)
friction_coeff = 0.7 # friction between tires and ground (guess from google)
cart_weight = 2 # (kg)
drag_coeff = 0#1/80 # coefficient of drag moving forwards, basically jsut a scaling constant
battery_voltage = 12

# path data
pointList = [[0,0],[61,0],[63,1],[64,3],[63,5],[61,6],[0,6],[-2,5],[-3,3],[-2,1]]

#[[0.0, 0.0], [-3.399217, 1.182335], [-8.978368, 1.958245], [-10.49324, 3.990386], [-10.1607, 7.759084], [-7.722135, 10.19765], [-4.28597, 11.6571], [-1.810453, 14.13262], [-0.369481, 16.29408], [1.810453, 18.86196], [5.72694, 19.93346], [9.772753, 19.5455], [13.06112, 17.66115], [14.13262, 15.48122], [13.39365, 13.55992], [10.6595, 12.15589], [6.392007, 12.67317], [2.586361, 12.37759], [-0.738961, 10.86272], [-2.179934, 8.498045], [-2.179934, 5.505255], [-0.258636, 4.470711], [2.660256, 4.359866], [5.505253, 5.357462], [7.315706, 6.909279], [9.791225, 8.608889], [13.33823, 8.922945], [15.40732, 7.574344], [15.59206, 4.433763], [14.37278, 1.699609], [10.75187, 0.554222], [6.465902, -0.332532], [3.54701, -0.443377]]

# variables
laps = 1 # to be implemented
max_segment_space = 1 # maximum distance in meters between two points on the pointList (will interpolate if not fulfilled)

# setup
radii = []
max_vs = []
ideal_vs = []
forces = []
work = []
power = []
times = []
g = 9.8


# format path to not have points too far away and to account for laps by repeating path
i = 0
while True:
    x1 = pointList[i-1]
    x2 = pointList[i]
    dx = math.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)
    if dx > max_segment_space:
        dvs = math.ceil(dx/max_segment_space)-1
        for j in range(dvs):
            x3 = [x1[0]+((x2[0]-x1[0])/dvs)*(j+1),x1[1]+((x2[1]-x1[1])/dvs)*(j+1)]
            pointList.insert(i+j, x3)
        i += dvs

    i += 1
    if i == len(pointList):
        break

i = 0
while True:
    if pointList[i-1] == pointList[i]:
        pointList.remove(pointList[i])
        i -= 1
    i += 1
    if i == len(pointList):
        break


# def function for use later
def get_radius(x1, y1, x2, y2, x3, y3):
    s1 = x1**2 + y1**2
    s2 = x2**2 + y2**2
    s3 = x3**2 + y3**2
    
    m11 = x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)

    if m11 == 0:
      return float('inf')

    m12 = s1*(y2 - y3) + s2*(y3 - y1) + s3*(y1 - y2)
    m13 = s1*(x2 - x3) + s2*(x3 - x1) + s3*(x1 - x2)

    x0 = 0.5 * m12 / m11
    y0 = -0.5 * m13 / m11
    
    radius = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    return radius

# calculate turn radius at each point
for i in range(len(pointList)):
    x1 = []
    x2 = pointList[i]
    x3 = []
    if i == 0:
        x1 = pointList[-1]
        x3 = pointList[i+1]
    if i > 0 and i < len(pointList)-1:
        x1 = pointList[i-1]
        x3 = pointList[i+1]
    else:
        x1 = pointList[i-1]
        x3 = pointList[0]

    radii.append(get_radius(x1[0],x1[1],x2[0],x2[1],x3[0],x3[1]))

# calculate max speeds by friction
for each in radii:
    max_vs.append(math.sqrt(friction_coeff*g*each))

# calculate max speeds with kart characteristics
ideal_vs = max_vs
for i in range(len(ideal_vs)):
    if i == 0:
        v1 = ideal_vs[i] = 0 # starting point always velocity of 0
        continue

    # get adjacent points
    v1 = ideal_vs[i-1]
    x1 = pointList[i-1]
    v2 = ideal_vs[i]
    x2 = pointList[i]
    
    # check against max speed
    if v2 > max_v:
        ideal_vs[i] = max_v

    # check against max acceleration
    dx = math.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)
    if (v1*(v2-v1)/dx+((v2-v1)**2)/dx) > max_a:
        t = (-v1+math.sqrt(v1**2+4*max_a*dx))/(2*max_a)
        ideal_vs[i] = v1+max_a*t
        times.append(t)
    else:
        a = (v1*(v2-v1)/dx+((v2-v1)**2)/dx)
        t = (-v1+math.sqrt(v1**2+4*a*dx))/(2*a)
        times.append(t)

# calculate force on kart at each point
for i in range(len(ideal_vs)):
    # assuming point spacing is sufficiently close so that acceleraton estimation can be over small time scale
    forces.append(drag_coeff*ideal_vs[i]**2+(ideal_vs[i] < max_v)*cart_weight*max_a)

# calculate work done at each point since last point (left-sum)
totalDist = [0]
totalWork = [0]
for i in range(len(forces)):
    w = 0
    if i != 0:
        x1 = pointList[i-1]
        x2 = pointList[i]
        dx = math.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)
        totalDist.append(totalDist[i-1]+dx)
        w = forces[i]*dx
        totalWork.append(totalWork[i-1]+w)

    work.append(w)

total = 0
for i in range(len(work)):
    dQ = work[i]/battery_voltage
    total += dQ

print(total)
print(sum(times))

### READ CSV DATA
f = open("test.csv","r")

fields = []
rows = []

# creating a csv reader object
csvreader = csv.reader(f)

# extracting field names through first row
fields = next(csvreader)

# extracting each data row one by one
for row in csvreader:
    rows.append(row)

dt = 0.2 # each row is 0.2 secs apart
work = [0]
times = []
for i in range(len(rows)):
    if i > 0:
        work.append(work[i-1]+float(rows[i][1])*dt)
    times.append(i/len(rows))


# get estimate of time taken in ideal case
timeEst = [0]
for i in range(len(pointList)):
    if i > 0:
        x1 = pointList[i-1]
        x2 = pointList[i]
        dx = math.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)
        timeEst.append(timeEst[-1]+dx/ideal_vs[i])


for i in range(len(timeEst)):
    timeEst[i] = timeEst[i]/timeEst[-1]

_, ax = plt.subplots()
ax.plot(timeEst, totalWork, color="orange", label="Predicted")
ax.plot(times, work, color="blue", label="Experimental")
ax.legend()
plt.xlabel("Time (s)")
plt.ylabel("Work Done (J)")
plt.title("Prediction/Test Comparison")
plt.show()

work_extrapolated = []
for each in times:
    closest = abs(each-timeEst[0])
    closesti = 0
    for i in range(len(timeEst)):
        if abs(each-timeEst[i]) < closest:
            closest = abs(each-timeEst[i])
            closesti = i

    work_extrapolated.append(totalWork[closesti])

# error analysis
slope, intercept, r, p, std_err = stats.linregress(work_extrapolated, work)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, work_extrapolated))

print(f"Slope: {round(slope,2)}, Intercept: {round(intercept,2)}, R: {round(r,4)}, P: {round(p,5)}, Standard Error: {round(std_err,4)}")

_, ax = plt.subplots()
ax.scatter(work_extrapolated, work)
ax.plot(work_extrapolated, mymodel, color="orange", label=f"y={round(slope,2)}x+{round(intercept,2)}, R^2={round(r**2,4)}")
ax.legend()
plt.xlabel("Predicted Energy")
plt.ylabel("Experimental Energy")
plt.title("Single Test Accuracy Analysis")
plt.show()