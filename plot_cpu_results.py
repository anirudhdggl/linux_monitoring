import matplotlib.pyplot as plt
import numpy as np

cpu_file = "/home/aduggal/instance_analysis/c5a.2xlarge/cpu_usage.txt"

timestamps = []
cpu0 = []
cpu1 = []
cpu2 = []
cpu3 = []
cpu4 = []
cpu5 = []
cpu6 = []
cpu7 = []

with open(cpu_file, 'r') as f:
    log_file_lines = f.readlines()

for line in log_file_lines:
    temp_data = line.split(',')
    if temp_data[1] == "cpu0":
        cpu0.append(float(temp_data[2]))
        timestamps.append(temp_data[0])
    elif temp_data[1] == "cpu1":
        cpu1.append(float(temp_data[2]))
    elif temp_data[1] == "cpu2":
        cpu2.append(float(temp_data[2]))
    elif temp_data[1] == "cpu3":
        cpu3.append(float(temp_data[2]))
    elif temp_data[1] == "cpu4":
        cpu4.append(float(temp_data[2]))
    elif temp_data[1] == "cpu5":
        cpu5.append(float(temp_data[2]))
    elif temp_data[1] == "cpu6":
        cpu6.append(float(temp_data[2]))
    elif temp_data[1] == "cpu7":
        cpu7.append(float(temp_data[2]))

plt.plot(timestamps, cpu0)
plt.plot(timestamps, cpu1)
plt.plot(timestamps, cpu2)
plt.plot(timestamps, cpu3)
plt.plot(timestamps, cpu4)
plt.plot(timestamps, cpu5)
plt.plot(timestamps, cpu6)
plt.plot(timestamps, cpu7)
plt.show()