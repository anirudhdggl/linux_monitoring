import datetime
import re
import time

cpu_records = {}
log_file = "/home/aduggal/Desktop/cpu_usage.txt"
cpu_usage_file = "/proc/stat"
cpu_line_pattern = re.compile("^cpu[0-9]+$")

def log_cpu(cpu_name: str, delta_iowait_time: int, delta_total_time: int):
    """
        Log the CPU percent to the output file
    """
    cpu_percent = (delta_iowait_time / delta_total_time) * 100
    with open(log_file, 'a+') as f:
        f.write(str(datetime.datetime.now()) + "," + cpu_name + "," + str(cpu_percent) + "\n")

while True:
    with open(cpu_usage_file, 'r') as f:
        stat_file_lines = f.readlines()
    
    for line in stat_file_lines:
        cpu_detail = line.split()

        # Do anything only if the line starts as "cpu1" or "cpu50"
        # which means that this line shows details for a very
        # specific processor (core)
        if cpu_line_pattern.match(cpu_detail[0]):

            # 5th column (excluding the first which is the name of
            # the CPU) of the CPU detail shows the iowait time
            iowait_cpu_time_since_bootup = int(cpu_detail[5])

            total_cpu_time_since_bootup = 0
            old_iowait = 0
            old_total = 0

            # Add all CPU times to get the total CPU time for a
            # core
            for i in range(1, len(cpu_detail)):
                total_cpu_time_since_bootup = total_cpu_time_since_bootup + int(cpu_detail[i])
            
            # If we already have a record for this CPU in our map
            # fetch the old value, else set the old value to 0
            if cpu_detail[0] in cpu_records.keys():
                old_iowait = cpu_records[cpu_detail[0]]["iowait"]
                old_total = cpu_records[cpu_detail[0]]["total"]
            else:
                cpu_records[cpu_detail[0]] = {
                    "iowait" : 0,
                    "total" : 0
                }
            
            # Find change in total and iowait CPU time to capture
            # CPU percent
            delta_iowait = iowait_cpu_time_since_bootup - old_iowait
            delta_total = total_cpu_time_since_bootup - old_total

            # Log CPU % in the log file
            log_cpu(cpu_detail[0], delta_iowait, delta_total)

            # Set the current value as the old values
            cpu_records[cpu_detail[0]]["iowait"] = iowait_cpu_time_since_bootup
            cpu_records[cpu_detail[0]]["total"] = total_cpu_time_since_bootup
    
    # Repeat after 0.5s
    time.sleep(0.5)