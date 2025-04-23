import math
import matplotlib.pyplot as plt
import csv
from scipy import stats

# profile data
max_v = 22 # velocity (m/s)
max_a = max_v/1.5 # acceleration (m/s^2)
friction_coeff = 0.7 # friction between tires and ground (guess from google)
cart_weight = 3 # (kg)
drag_coeff = 0#1/80 # coefficient of drag moving forwards, basically jsut a scaling constant
battery_voltage = 12.6

# path data
# parking lot path
pointList = [[0.0,0.0],[11.8640031814575,0.123588383197784],[24.0987548828125,-0.123576648533344],[39.2995147705078,-1.48300182819366],[55.9832649230957,-1.35941350460052],[70.1953506469727,-1.11224842071533],[80.0820236206055,0.865083456039429],[87.3734359741211,7.04425573348999],[90.5866012573242,12.9762516021729],[90.8337631225586,19.5261726379395],[88.2385177612305,22.7393398284912],[83.6659393310547,23.3572521209717],[77.1160202026367,24.4695072174072],[72.0491027832031,26.3232555389404],[67.4765167236328,29.1656723022461],[62.780345916748,33.2439231872559],[59.8143501281738,37.1985931396484],[58.0841827392578,42.1419219970703],[58.207763671875,45.2315101623535],[59.4435997009277,47.9503440856934],[62.2860145568848,50.7927665710449],[66.3642654418945,51.9050140380859],[73.0377655029297,52.6465110778809],[77.3631896972656,56.2304382324219],[81.5650177001953,60.0615158081055],[86.8791046142578,66.611442565918],[90.0922698974609,72.7906036376953],[89.3507690429688,76.7452697753906],[87.0026931762695,78.9697723388672],[81.4414367675781,79.4641036987305],[72.4198532104492,79.8348541259766],[62.0388488769531,80.2056045532227],[50.6691741943359,79.7112731933594],[36.5806770324707,79.7112731933594],[26.9411678314209,80.0820159912109],[14.8300065994263,80.0820159912109],[6.67350292205811,80.0820159912109],[1.73016691207886,79.7112731933594],[-3.70749878883362,78.7226104736328],[-7.66216897964478,76.6216888427734],[-10.7517490386963,73.7792663574219],[-12.2347507476807,69.4538497924805],[-12.9762516021729,62.0388565063477],[-12.3583335876465,54.9946022033691],[-11.1225023269653,46.5909309387207],[-10.7517490386963,39.9174270629883],[-10.7517490386963,34.9740905761719],[-10.9989137649536,28.6713428497314],[-10.504584312439,21.997838973999],[-9.14516448974609,15.4479188919067],[-8.77441692352295,8.4036693572998],[-7.41499757766724,3.95466375350952],[-4.69616460800171,1.60659027099609]]

# simple down and back
#[[0,0],[61,0],[63,1],[64,3],[63,5],[61,6],[0,6],[-2,5],[-3,3],[-2,1]]

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

removed = 0
i = 0
while True:
    x1 = pointList[i-1]
    x2 = pointList[i]
    dx = abs(math.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2))
    if dx < 0.0001:
        #print(pointList[i],pointList[i-1])
        pointList.remove(pointList[i])
        i -= 1
        removed += 1
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
        t = 0
        if a > 0:
            t = (-v1+math.sqrt(v1**2+4*a*dx))/(2*a)
        else:
            t = dx/v1
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

print(f"Energy Used: {total}")
print(f"Estimated Time: {sum(times)}")

### READ CSV DATA
f = open("parkinglotpath.csv","r")

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

print(f"Accuracy: {100-100*abs(totalWork[-1]-work[-1])/work[-1]}%")

_, ax = plt.subplots()
ax.plot(timeEst, totalWork, color="orange", label="Predicted")
ax.plot(times, work, color="blue", label="Experimental")
ax.legend()
plt.xlabel("Percentage Time")
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