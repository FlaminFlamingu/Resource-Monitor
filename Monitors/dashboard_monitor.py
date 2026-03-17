"""
FILE DESCRIPTION KEY COMPONENTS:
1. DATA FETCH: Retrieves CPU, RAM, and GPU percentages.
2. STORAGE LOGIC: Sums all system drives to provide a unified total capacity and usage.
"""

"""
LIBRARIES USED:
1. psutil: Core hardware interaction.
2. GPUtil: NVIDIA GPU data retrieval.
"""

import psutil
try:
    import GPUtil
    HAS_GPU = True
except ImportError:
    HAS_GPU = False

def get_dashboard_metrics():
    # Gathers raw system data for the dashboard components
    metrics = {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "gpu": "N/A",
        "storage_pct": 0.0,
        "storage_total": 0
    }

    if HAS_GPU:
        gpus = GPUtil.getGPUs()
        if gpus:
            metrics["gpu"] = gpus[0].load * 100

    total_used = 0
    total_cap = 0
    for part in psutil.disk_partitions():
        if 'fixed' in part.opts or part.fstype:
            try:
                usage = psutil.disk_usage(part.mountpoint)
                total_used += usage.used
                total_cap += usage.total
            except: continue
    
    if total_cap > 0:
        metrics["storage_pct"] = (total_used / total_cap) * 100
        metrics["storage_total"] = total_cap / (1024**3)

    return metrics