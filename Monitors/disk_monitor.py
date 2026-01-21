"""Disk Storage Monitoring Module

This module monitors all disk partitions and storage devices on the system. It collects
information about device names, mount points, total capacity, used space, and usage percentage
for each disk partition with a valid file system.

Functions:
- get_disk_stats(): Returns a list of dictionaries containing disk information for all partitions
"""

import psutil

def get_disk_stats():
    disks = []
    for partition in psutil.disk_partitions():
        if partition.fstype:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mount": partition.mountpoint,
                    "total": round(usage.total / (1024**3), 1),
                    "used": round(usage.used / (1024**3), 1),
                    "percent": usage.percent
                })
            except:
                continue
    return disks