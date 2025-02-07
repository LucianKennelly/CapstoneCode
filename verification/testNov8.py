import csv
import matplotlib.pyplot as plt
from mpl_toolkits import axisartist
from mpl_toolkits.axes_grid1 import host_subplot
from scipy import stats

f = open("testNov8.csv","r")

fields = []
rows = []

# creating a csv reader object
csvreader = csv.reader(f)

# extracting field names through first row
fields = next(csvreader)

# extracting each data row one by one
for row in csvreader:
    rows.append(row)

t = []
current = []
voltage = []
resistance = []
velocity = []
#convert mph to m/s
for i in range(len(rows)):
    for j in range(len(rows[i])):
        rows[i][j] = float(rows[i][j])
    rows[i][4] = rows[i][4]/2.237
    t.append(rows[i][0])
    current.append(rows[i][1])
    voltage.append(rows[i][2])
    resistance.append(rows[i][3])
    velocity.append(rows[i][4])

vars = [current,voltage,resistance,velocity]
labels = ["Current (A)", 'Voltage (V)', 'Resistance (Ohms)', 'Velocity (m/s)']
colors = ["tab:red","tab:orange","tab:green","tab:blue","tab:purple"]

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

p1, = host.plot(t, vars[3], label=labels[3])
p2, = par1.plot(t, vars[0], label=labels[0])
p3, = par2.plot(t, vars[1], label=labels[1])
p4, = par2.plot(t, vars[2], label=labels[2])

host.set(xlim=(0, 20), ylim=(0, 45), xlabel="Time", ylabel=labels[3])
par1.set(ylim=(0, 45), ylabel=labels[0])
par2.set(ylim=(0, 25), ylabel=labels[1])
par3.set(ylim=(0, 25), ylabel=labels[2])

host.legend()

host.axis["left"].label.set_color(p1.get_color())
par1.axis["left"].label.set_color(p2.get_color())
par2.axis["right"].label.set_color(p3.get_color())
par3.axis["right"].label.set_color(p4.get_color())


plt.title("November 8, 2024 Test Data")
plt.show()


# prediction example:
w_real = [] # work done, i.e. power drained in joules
position = [] # distance moved since last timestep
mass = 3.111 # weight in kg
acceleration = []
force = []
times = t
scale_const = 1

for i in range(len(rows)):
    c = rows[i][1]
    v = rows[i][2]
    t = rows[i][0]
    vl = rows[i][4]
    a = vl
    dt = t
    prev = 0
    if i > 0:
        t -= rows[i-1][0]
        prev = w_real[i-1]
        a -= rows[i-1][4]
        if a < 0:
            a = 0
    position.append(v*t)
    acceleration.append(a)
    force.append(vl**2+mass*a)
    w_real.append(prev+c*v*t)

print(position)
print(acceleration)
print(force)

w_predict = [] #prediction
for i in range(len(rows)):
    w = force[i]*position[i]*scale_const
    if i > 0:
        w += w_predict[i-1]
    w_predict.append(w)

slope, intercept, r, p, std_err = stats.linregress(w_predict, w_real)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, w_predict))

print(f"Slope: {round(slope,2)}, Intercept: {round(intercept,2)}, R: {round(r,10)}, P: {round(p,10)}, Standard Error: {round(std_err,10)}")

plt.scatter(w_predict, w_real)
plt.plot(w_predict, mymodel)
plt.title("Prediction vs Actual Work (J)")
plt.xlabel("Predicted Work")
plt.ylabel("Actual Work (J)")
plt.show()

for i in range(len(w_predict)):
    w_predict[i] *= slope

fig, ax = plt.subplots()
ax.scatter(times, w_predict, c="tab:blue", label="Predicted")
ax.scatter(times, w_real, c="tab:green", label="Actual")
ax.legend()
plt.xlabel("Time (s)")
plt.ylabel("Predicted and Actual Work (J)")
plt.show()