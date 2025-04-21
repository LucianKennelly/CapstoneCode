import csv
import math
import matplotlib.pyplot as plt

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
        work.append(work[i-1]+int(rows[i][1])/dt)
    times.append(i*2)

plt.plot(times, work)
plt.xlabel("Time (s)")
plt.ylabel("Work Done (J)")
plt.show()