import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
import tkinter as tk
#import testNov8
data = open("..\verification\gui.py")
timepoints = data.times
data.w_real
timepoints = np.array([8,1])
voltagepoints = np.array([0,1])
fig, ax= plt.subplots()
plt.subplots_adjust(bottom=0.35)
plt.plot(timepoints,voltagepoints)
plt.xlabel('Time (min)')
plt.ylabel('State of Charge (C)')
m = 0
axm = plt.axes([0.25,0.2,0.65,0.03])
mass = Slider(axm,'Mass (kg)',0,2000)
resetax = plt.axes([0.8,0.025,0.1,0.04])
button = Button(resetax,'Run Test', color="gold",hovercolor='skyblue')
root = tk.Tk()
P = 1000
tk.Label(root,text=("Power Consumption (W): ",P,"(W)")).pack()
def update(val):
    m = mass.val
mass.on_changed(update)
def resetSlider(event):
    mass.reset()
button.on_clicked(resetSlider)
plt.show()