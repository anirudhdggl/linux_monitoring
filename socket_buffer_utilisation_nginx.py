"""
    The following code will first find the master process ID for nginx. Then
    it will look for nginx worker processes for that master process. Once we
    have the PIDs of the worker process, we can access details like their
    TCP memory usage - which is basically the size of their TCP buffer (receive
    + transmit) and some connection data. This would be in the form of memory
    pages. So an output of 9 will mean we have allocated 9 memory pages for the
    buffer. A memory page is usually 4KB in size.
"""

import time
import datetime
import os
import re

nginx_pid_file_path = "/var/run/nginx.pid" # This file contains the pid for the nginx master process
output_file = "/home/aduggal/Desktop/buffer_size" # output file to write data to


def get_nginx_master_pid() -> int:
    with open(nginx_pid_file_path, 'r') as f:
        #TODO: Error handling in case a new line char is present
        # at the end of the pid in the file
        pid = f.readline()
    return int(pid)


def get_nginx_children_pid() -> list:
    nginx_master_pid = get_nginx_master_pid()

    # This path contains the pids of the children processes of a process
    nginx_children_proc_file = "/proc/" + str(nginx_master_pid) + "/task/" + str(nginx_master_pid) + "/children"

    with open(nginx_children_proc_file, 'r') as f:
        children_pids = f.readline()
    
    return children_pids.split()


def used_memory_pages_in_socket_buffer(pid: int) -> int:
    
    # This file contains the socket details for a process
    # The last value, mem is the number of memory pages used
    # by the socket
    
    proc_file = "/proc/" + str(pid) + "/net/sockstat"
    with open(proc_file, 'r') as f:
        file_data = f.readlines()
    
    # Find only for TCP sockets
    for line in file_data:
        temp = line.split()
        if temp[0] == "TCP:":
            pages = temp[-1]
            return int(pages)


def get_nginx_worker_pid() -> list:
    worker_process_re = re.compile(r'worker')
    nginx_children_pid = get_nginx_children_pid()
    nginx_worker_pid = []

    for pid in nginx_children_pid:

        # Find the command name if it is worker or something else
        procfs_cmd_path = "/proc/" + str(pid) + "/cmdline"
        
        with open(procfs_cmd_path, 'r') as f:
            cmd_name = f.readline()
        
        if worker_process_re.search(cmd_name):
            nginx_worker_pid.append(pid)
    
    return nginx_worker_pid


worker_processes = get_nginx_worker_pid()

while True:
    for pid in worker_processes:

        # Check if directory for the worker process ID exist
        # or not. If not then nginx might have been restarted
        # and may have different process IDs
        if not os.path.isdir("/proc/"+str(pid)):
            worker_processes = get_nginx_worker_pid()
            break
    
    page_usage = []

    for pid in worker_processes:
        page_usage.append(used_memory_pages_in_socket_buffer(int(pid)))

    with open(output_file, 'a+') as f:
        output_line = ' '.join(str(elem) for elem in page_usage)
        f.write(str(datetime.datetime.now()) + "," + output_line + "\n")
    
    # Collect every 0.5s
    time.sleep(0.5)