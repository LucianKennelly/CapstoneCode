import csv
import matplotlib.pyplot as plt
from mpl_toolkits import axisartist
from mpl_toolkits.axes_grid1 import host_subplot
from scipy import stats


def getVerificationData(filename):
    try:
        f = open(filename,"r")
    except:
        print("File does not exist")
        return (-1,-1,-1)

    fields = []
    rows = []

    # creating a csv reader object
    csvreader = csv.reader(f)

    # extracting field names through first row
    fields = next(csvreader)
    if (len(fields) != 5):
        print("Invalid data fields. Please format as: Time, Current (A), Voltage (V), Resistance (Ohms), Velocity (mph)")
        return (-1,-1,-1)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    times = []
    current = []
    voltage = []
    resistance = []
    velocity = []
    #convert mph to m/s
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j] = float(rows[i][j])
        rows[i][4] = rows[i][4]/2.237
        times.append(rows[i][0])
        current.append(rows[i][1])
        voltage.append(rows[i][2])
        resistance.append(rows[i][3])
        velocity.append(rows[i][4])

    vars = [current,voltage,resistance,velocity]
    #labels = ["Current (A)", 'Voltage (V)', 'Resistance (Ohms)', 'Velocity (m/s)']

    return (vars, times, fields)


def showVerificationData(vars, times, fields):
    host = host_subplot(111, axes_class=axisartist.Axes)
    plt.subplots_adjust(left=0.2,right=0.8)

    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()

    par1.axis["left"] = par1.new_fixed_axis(loc="left", offset=(-50, 0))
    par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(0, 0))
    par3.axis["right"] = par3.new_fixed_axis(loc="right", offset=(50, 0))

    par1.axis["left"].toggle(all=True)
    par2.axis["right"].toggle(all=True)
    par3.axis["right"].toggle(all=True)

    p1, = host.plot(times, vars[3], label=fields[3])
    p2, = par1.plot(times, vars[0], label=fields[0])
    p3, = par2.plot(times, vars[1], label=fields[1])
    p4, = par2.plot(times, vars[2], label=fields[2])

    host.set(xlim=(0, 20), ylim=(0, 45), xlabel="Time", ylabel=fields[3])
    par1.set(ylim=(0, 45), ylabel=fields[0])
    par2.set(ylim=(0, 25), ylabel=fields[1])
    par3.set(ylim=(0, 25), ylabel=fields[2])

    host.legend()

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["left"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())
    par3.axis["right"].label.set_color(p4.get_color())


    plt.title("Data")
    plt.show()


def calculateScale(vars, times, showGraph):
    # prediction example:
    real = [] # work done, i.e. power drained in joules
    position = [] # distance moved since last timestep
    mass = 3.111 # weight in kg
    acceleration = []
    force = []
    scale_const = 1

    # format data ito rows
    rows = []
    for i in range(len(times)):
        row = [times[i]]
        for each in vars:
            row.append(each[i])
        rows.append(row)

    # calculations for each timestamp
    for i in range(len(rows)):
        c = rows[i][1]
        v = rows[i][2]
        t = rows[i][0]
        vl = rows[i][4]
        a = vl
        prev = 0
        if i > 0:
            t -= rows[i-1][0]
            prev = real[i-1]
            a -= rows[i-1][4]
            if a < 0:
                a = 0
        position.append(v*t)
        acceleration.append(a)
        force.append(vl**2+mass*a)
        real.append(prev+c*v*t)

    #print(position)
    #print(acceleration)
    #print(force)

    prediction = [] # work prediction
    for i in range(len(rows)):
        w = force[i]*position[i]*scale_const
        if i > 0:
            w += prediction[i-1]
        prediction.append(w)

    slope, intercept, r, p, std_err = stats.linregress(prediction, real)

    # print calculated relation info
    # slope will be used as scaling constant
    print(f"Slope: {round(slope,2)}, Intercept: {round(intercept,2)}, R: {round(r,10)}, P: {round(p,10)}, Standard Error: {round(std_err,10)}")

    if (showGraph):
        showScaleGraph(prediction, real, slope, intercept)

    # scale prediction in for example display
    for i in range(len(prediction)):
        prediction[i] *= slope

    return (slope, prediction, real)

def showScaleGraph(prediction, real, scale, intercept):
    def myfunc(x):
        return scale * x + intercept

    model = list(map(myfunc, prediction))

    plt.scatter(prediction, real)
    plt.plot(prediction, model)
    plt.title("Prediction vs Actual Work (J)")
    plt.xlabel("Predicted Work")
    plt.ylabel("Actual Work (J)")
    plt.show()

def showPredictionAccuracy(times, prediction, real):   
    _, ax = plt.subplots()
    ax.scatter(times, prediction, c="tab:blue", label="Predicted")
    ax.scatter(times, real, c="tab:green", label="Actual")
    ax.legend()
    plt.xlabel("Time (s)")
    plt.ylabel("Predicted and Actual Work (J)")
    plt.show()

# makes a prediction from a position data file
def makePrediction(inputFile):
    pass


def main():
    fileAsk = '''
Welcome to the EVGPal calibrator. Please select a file containing verification data
    
File: '''

    mainPage = '''
Please select a function:

    1. Display Data
    2. Calculate Scaling Constant
    3. Display Sample Prediction
    4. Make Prediction
    5. Print Scaling Constant
    6. Select a New File
    7. Exit

Selection: '''
    vars = []
    times = []
    fields = []

    file_in = input(fileAsk)
    vars, times, fields = getVerificationData(file_in)
    while (vars == -1):
        file_in = input("File: ")
        vars, times, fields = getVerificationData(file_in)
    
    prediction = []
    real = []
    scale = 0

    while True:
        num = input(mainPage)

        while (not num.isnumeric()) or (not int(num) in [1,2,3,4,5]):
            num = input("Please ender a valid number: ")

        num = int(num)

        # match case was throwing an error, not sure why
        if num==1:
            showVerificationData(vars, times, fields)
            
        elif num==2:
            showGraph = ""
            while not showGraph in ["y","n"]:
                showGraph = input("Would you like to display the data graphically? (Y/N): ").lower()
            scale, prediction, real = calculateScale(vars, times, showGraph=='y')

        elif num==3:
            if scale == 0:
                scale, prediction, real = calculateScale(vars, times, False)
            showPredictionAccuracy(times, prediction, real)

        elif num==4:
            file_in = input("Position Data File: ")
            while (makePrediction(file_in) == -1):
                file_in = input("Position Data File: ")

        elif num==5:
            if scale == 0:
                scale, prediction, real = calculateScale(vars, times, False)
            print(scale)

        elif num==6:
            scale = 0
            vars = -1
            while (vars == -1):
                file_in = input("File: ")
                vars, times, fields = getVerificationData(file_in)
        else:
            break
        
main()