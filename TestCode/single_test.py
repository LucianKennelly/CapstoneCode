import math
import matplotlib.pyplot as plt
import csv
from scipy import stats

# def function for use later
def get_radius(x1, y1, x2, y2, x3, y3):
    s1 = x1**2 + y1**2
    s2 = x2**2 + y2**2
    s3 = x3**2 + y3**2
    
    m11 = x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)

    if m11 == 0:
      return 10000.0

    m12 = s1*(y2 - y3) + s2*(y3 - y1) + s3*(y1 - y2)
    m13 = s1*(x2 - x3) + s2*(x3 - x1) + s3*(x1 - x2)

    x0 = 0.5 * m12 / m11
    y0 = -0.5 * m13 / m11
    
    radius = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    return radius

# full test
def runTest(pointList, verification_file, profile, laps, friction_coeff, max_segment_space, showTimeGraph, showAnalysisGraph):
    max_v, max_a, cart_weight, drag_coeff, battery_voltage, brake_speed = profile

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

    # duplicate path for laps
    pointListOG = pointList.copy()
    for i in range(laps-1):
        pointList.extend(pointListOG.copy())


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

    # calculate safe braking speeds
    # start 1 from end, back propogate
    for i in range(len(ideal_vs)-2, -1, -1):
        v1 = ideal_vs[i]
        v2 = ideal_vs[i+1]
        dx = math.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)
        if (v1-v2)/times[i] > brake_speed: # if braking too fast
            t = (-v2+math.sqrt(v2**2+4*brake_speed*dx))/(2*brake_speed)
            ideal_vs[i] = ideal_vs[i+1]+brake_speed*t

    # calculate force on kart at each point
    for i in range(len(ideal_vs)):
        # assuming point spacing is sufficiently close so that acceleraton estimation can be over small time scale
        a = max_a
        if i > 0:
            a = abs(ideal_vs[i-1]-ideal_vs[i])/times[i-1]
        forces.append(drag_coeff*ideal_vs[i]**2+cart_weight*a)

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

    total_charge = 0
    for i in range(len(work)):
        dQ = work[i]/battery_voltage
        total_charge += dQ

    print(f"Estimated Time: {sum(times)}")
    print(f"Est. Battery life: {(6800/(total_charge/3.6))*(sum(times)/60)} mins")

    ### READ CSV DATA
    f = open(verification_file,"r")

    fields = []
    rows = []


    # creating a csv reader object
    csvreader = csv.reader(f)

    # extracting field names through first row
    #fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    ### FORMATTING TIMES FOR GRAPH
    # get estimate of time taken in ideal case
    timeEst = [sum(times[0:i]) for i in range(1,len(times)+1)]
    timeEst.insert(0,0)
    timeEst = [each/timeEst[-1] for each in timeEst]

    dt = 0.2 # each row is 0.2 secs apart
    work = [0]
    times = []
    for i in range(len(rows)):
        if i > 0:
            work.append(work[i-1]+abs(float(rows[i][2])*float(rows[i][4]))*dt)
        times.append(i/len(rows))

    # output some stats that need loaded data
    print(f"Calc. Battery life: {(6800/((work[-1]/battery_voltage)/3.6))*(times[-1]/60)} mins")
    print(f"Accuracy: {100-100*abs(totalWork[-1]-work[-1])/work[-1]}%")

    if showTimeGraph:
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

    if showAnalysisGraph:
        _, ax = plt.subplots()
        ax.scatter(work_extrapolated, work)
        ax.plot(work_extrapolated, mymodel, color="orange", label=f"y={round(slope,2)}x+{round(intercept,2)}, R^2={round(r**2,4)}")
        ax.legend()
        plt.xlabel("Predicted Energy (J)")
        plt.ylabel("Experimental Energy (J)")
        plt.title("Single Test Accuracy Analysis")
        plt.show()

    # returns predicted value and actual value
    return (totalWork[-1], work[-1])