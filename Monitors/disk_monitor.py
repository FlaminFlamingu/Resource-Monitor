"""
FILE DESCRIPTION:
This module monitors all disk partitions and storage devices on the system. 
It identifies active drives, their mount points (e.g., C:\), and tracks 
how much space is currently occupied versus the total capacity.
"""

"""
LIBRARY DESCRIPTIONS:
- psutil: (Process and System Utilities) A library used here to query 
          physical disk partitions and calculate storage usage data.
"""

import psutil # Library for retrieving hardware and disk utilization stats

def get_disk_stats():
    # List to store the information for every detected drive
    disks = []
    
    # Iterate through all hardware partitions recognized by the OS
    for partition in psutil.disk_partitions():
        # Only process partitions that have a valid file system (skips empty drives)
        if partition.fstype:
            try:
                # Retrieve specific usage data for the current mount point
                usage = psutil.disk_usage(partition.mountpoint)
                
                disks.append({
                    "device": partition.device,
                    "mount": partition.mountpoint,
                    # Convert bytes to Gigabytes (GB) for readability
                    "total": round(usage.total / (1024**3), 1),
                    "used": round(usage.used / (1024**3), 1),
                    "percent": usage.percent
                })
            except:
                # Skip drives that might be locked or inaccessible (like some CD-ROMs)
                continue
                
    return disks