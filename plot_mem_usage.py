import matplotlib.pyplot as plt

cpu_file = "/home/aduggal/Downloads/mem_output.txt"

timestamps = []
mem = []

with open(cpu_file, 'r') as f:
    log_file_lines = f.readlines()

for line in log_file_lines:
    temp_data = line.split(',')
    timestamps.append(temp_data[0])
    mem.append(float(temp_data[1]))

plt.plot(timestamps, mem)
plt.show()