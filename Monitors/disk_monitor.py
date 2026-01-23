"""
FILE DESCRIPTION:
This module monitors fixed internal storage devices. It is specifically 
configured to filter out removable media (USBs) to ensure that 
long-term storage data remains separated from hot-plug events.
"""

"""
LIBRARY DESCRIPTIONS:
- psutil: Used to query system disk partitions and usage. We use the 
          'opts' attribute here to identify and skip removable drives.
"""

import psutil # Library for hardware and storage utilization stats

def get_disk_stats():
    # List to store information for fixed internal drives only
    disks = []
    
    # Iterate through partitions and filter for fixed hardware
    for partition in psutil.disk_partitions():
        # FILTER: Only include partitions with a filesystem that ARE NOT 'removable'
        if partition.fstype and 'removable' not in partition.opts:
            try:
                # Retrieve usage data for the internal mount point
                usage = psutil.disk_usage(partition.mountpoint)
                
                disks.append({
                    "device": partition.device,
                    "mount": partition.mountpoint,
                    # Convert bytes to Gigabytes (GB)
                    "total": round(usage.total / (1024**3), 1),
                    "used": round(usage.used / (1024**3), 1),
                    "percent": usage.percent
                })
            except:
                # Skip drives that are locked by the system
                continue
                
    return disks