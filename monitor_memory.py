import datetime
import time

stats_file = "/proc/meminfo"
log_file = "/home/aduggal/mem_monit/mem_output.txt"

while True:
    with open(stats_file, 'r') as f:
        stat_file_lines = f.readlines()

    total_memory = 0
    available_memory = 0

    for line in stat_file_lines:
        detail = line.split()
        if detail[0] == "MemTotal:":
            total_memory = float(detail[1])
        elif detail[0] == "MemAvailable:":
            available_memory = float(detail[1])

    mem_utilisation = (total_memory - available_memory) * 100 / total_memory

    with open(log_file, 'a+') as f:
        f.write(str(datetime.datetime.now()) + "," + str(mem_utilisation) + "\n")
    
    time.sleep(0.5)