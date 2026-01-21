"""
FILE DESCRIPTION:
This module tracks system memory (RAM) usage statistics. It monitors 
the total capacity, current consumption, and overall utilization 
percentage of the system's physical memory.
"""

"""
LIBRARY DESCRIPTIONS:
- psutil: A cross-platform library for retrieving information on 
          running processes and system utilization (CPU, memory, disks, network, sensors).
"""

import psutil # Library used to access system hardware and memory stats

def get_memory_stats():
    # Gathers virtual memory statistics and converts bytes into Gigabytes (GB)
    mem = psutil.virtual_memory()
    return {
        # Calculation: bytes / 1024^3 = Gigabytes
        "total": round(mem.total / (1024**3), 1),
        "used": round(mem.used / (1024**3), 1),
        "percent": mem.percent
    }