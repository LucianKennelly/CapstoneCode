import csv
import matplotlib.pyplot as plt
from mpl_toolkits import axisartist
from mpl_toolkits.axes_grid1 import host_subplot

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
