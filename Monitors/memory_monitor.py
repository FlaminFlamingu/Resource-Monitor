"""Memory Monitoring Module

This module tracks system memory (RAM) usage statistics including total memory capacity,
current memory usage, and memory utilization percentage. All values are converted to
gigabytes for improved readability.

Functions:
- get_memory_stats(): Returns a dictionary with total memory, used memory, and usage percentage
"""

import psutil

def get_memory_stats():
    mem = psutil.virtual_memory()
    return {
        "total": round(mem.total / (1024**3), 1),
        "used": round(mem.used / (1024**3), 1),
        "percent": mem.percent
    }