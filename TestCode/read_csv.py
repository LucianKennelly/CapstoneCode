import csv
import math
import matplotlib.pyplot as plt

f = open("data_logs/yellow.csv","r")

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
work2 = [0]
times = []
vs = []
for i in range(len(rows)):
    if i > 0:
        #work.append(work[i-1]+float(rows[i][1])*dt*10)
        work2.append(work2[i-1]+float(rows[i][2])*float(rows[i][4]))
    times.append(i*2)
    vs.append(int(rows[i][6]))


#plt.plot(times, [each/work[-1] for each in work])
plt.plot(times, [each/work2[-1] for each in work2])
plt.xlabel("Time (s)")
plt.ylabel("Work Done (J)")
plt.show()