import datetime
import time

net_data_file_path = "/proc/net/dev"
output_file_path = "/home/aduggal/Desktop/output"
interface = "wlp2s0"
incoming_bytes = 0

while True:
    with open(net_data_file_path, 'r') as f:
        network_details = f.readlines()

    for x in network_details:
        temp_data = x.split()
        
        # Find data only in required interface
        if temp_data[0] == (interface+":"):
            incoming_bytes = temp_data[1]

    with open(output_file_path, 'a+') as f:
        f.write(str(datetime.datetime.now()) + ", " + incoming_bytes + '\n')
    
    time.sleep(0.5)

# Run the following to add it to crontab for every reboot
# @reboot nohup python3.8 /home/erpuser/network_monitoring/capture_network_traffic/capture_data.py &