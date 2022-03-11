import datetime
import time

stat_file = "/proc/stat"
log_file = "/home/aduggal/cpu_monit/blocked_procs.txt"
# log_file = "/home/aduggal/Desktop/proc_blocked.txt"
interval = 0.5 # Interval to collect metrics in seconds

def log_blocked_procs(blocked_proc: str):
    with open(log_file, 'a+') as f:
        f.write(str(datetime.datetime.now()) + "," + blocked_proc + "\n")

while True:
    with open(stat_file, 'r') as f:
        stat_file_lines = f.readlines()

    for line in stat_file_lines:
        temp_data = line.split()
        if temp_data[0] == "procs_blocked":
            log_blocked_procs(temp_data[1])
    
    time.sleep(interval)