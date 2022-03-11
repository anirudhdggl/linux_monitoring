"""
    This script will plot metrics stored in
    different files - which basically be in
    most cases different metrics and compare
    them on the same graph.

    These file paths will be passed in the
    form of a 2-D list, with each list having
    another list of path, metric index. This
    is because metrics are at index 2 for CPU
    while 1 for all other metrics.

    The data in files should be comma-separated

    Aggregation interval = 1 minute (max)

    NOTE: Only add the file to fetch_timestamps
    whose timestamp you give preference to - that
    is the time window
"""

# List format:
# [[filepath, index], [filepath, index]]

files = [["/home/aduggal/Downloads/iowait.txt", 2], ["/home/aduggal/Downloads/cpu_usage.txt", 2]]

# def aggregate(file_path: str, index: int):

def fetch_timestamps(file_path: str) -> map:
    """
        This function makes a basic assumption that
        timestamp will be the first thing in each
        metric line and will be of the following format
        
        2022-02-10 09:23:57.849788
    """
    with open(file_path, 'r') as f:
        file_lines = f.readlines()
    
    timestamp_map = {}

    for line in file_lines:
        timestamp = line.split(',')[0].split()[1].split(':')
        hh = timestamp[0]
        mm = timestamp[1]
        map_key = hh + mm

        if map_key not in timestamp_map.keys():
            timestamp_map[map_key] = -1
    
    return timestamp_map


metric_indices = []
file_paths = []

for file_info in files:
    file_paths.append(file_info[0])
    metric_indices.append(file_info[1])

for i in range(0, len(metric_indices)):
    
