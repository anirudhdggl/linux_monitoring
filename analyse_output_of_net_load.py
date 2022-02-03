import matplotlib.pyplot as plt

output_file = "/home/aduggal/Desktop/traffic-31-jan-16-25"
old_value = 0
timestamp_val = []
bytes_val = []

with open(output_file, 'r') as f:
    data_points = f.readlines()

for data in data_points:
    temp = data.split(',')
    total_bytes_transferred = int(temp[1][:-1])
    bytes_transferred_now = (total_bytes_transferred - old_value) / (1024)
    old_value = total_bytes_transferred
    # print(temp[0] + ": " + str(bytes_transferred_now) + " KB")
    timestamp_val.append(temp[0])
    bytes_val.append(bytes_transferred_now)

bytes_val[0] = 0
plt.plot(timestamp_val, bytes_val)
plt.show()