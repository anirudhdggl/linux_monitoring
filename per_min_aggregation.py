# This assumes that the log collection duration is 
# LESS THAN 1 DAY

import matplotlib.pyplot as plt
import numpy as np

log_file = "/home/aduggal/Downloads/cpu_usage.txt"
cores = 2
cpu_map = {}
cpu_list = []
timestamps = []

with open(log_file, 'r') as f:
    log_file_lines = f.readlines()

for line in log_file_lines:
    temp = line.split(',')
    cpu_util = float(temp[2])
    log_time = temp[0].split()[1]
    hh_mm = log_time.split(':')[0] + log_time.split(':')[1]
    # print(hh_mm + "\n")
    if hh_mm in cpu_map.keys():
        if cpu_map[hh_mm] < cpu_util:
            cpu_map[hh_mm] = cpu_util
    else:
        cpu_map[hh_mm] = cpu_util
        timestamps.append(hh_mm)

for k in cpu_map.keys():
    cpu_list.append(cpu_map[k])

log_file = "/home/aduggal/Downloads/iowait.txt"
iowait_list = []

cpu_map = {}
with open(log_file, 'r') as f:
    log_file_lines = f.readlines()

for line in log_file_lines:
    temp = line.split(',')
    cpu_util = float(temp[2])
    log_time = temp[0].split()[1]
    hh_mm = log_time.split(':')[0] + log_time.split(':')[1]
    # print(hh_mm + "\n")
    if hh_mm in cpu_map.keys():
        if cpu_map[hh_mm] < cpu_util:
            cpu_map[hh_mm] = cpu_util
    else:
        cpu_map[hh_mm] = cpu_util
        # timestamps.append(hh_mm)

for k in cpu_map.keys():
    iowait_list.append(cpu_map[k])

fig, ax1 = plt.subplots()
ax1.plot(timestamps, cpu_list, color = 'green', label = 'CPU %')
ax2 = ax1.twinx()
ax2.plot(timestamps, iowait_list, color = 'blue', label = 'IOWait CPU %', linestyle='dashed')

# plt.plot(timestamps, cpu_list)
# plt.plot(timestamps, iowait_list)
plt.show()