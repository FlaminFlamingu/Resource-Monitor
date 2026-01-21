"""GPU Monitoring Module

This module retrieves GPU statistics from NVIDIA and AMD graphics cards, including GPU load,
memory usage, and temperature. It utilizes multiple libraries (WMI, ADLManager, and GPUtil)
to gather comprehensive GPU data, with fallback mechanisms for handling unavailable metrics.

Functions:
- get_gpu_stats(): Returns a list of dictionaries containing GPU information for all detected GPUs
"""

import GPUtil
from pyadl import ADLManager 
import wmi

def get_gpu_stats():
    master_gpus = {}

    try:
        w = wmi.WMI()
        for gpu in w.Win32_VideoController():
            name = gpu.Name
            if "Intel" in name: 
                continue
            
            vram_mb = abs(int(int(gpu.AdapterRAM or 0) / (1024**2)))
            
            master_gpus[name] = {
                "name": name,
                "load": 0.0,
                "memory_total": vram_mb,
                "memory_used": "N/A",
                "temp": "N/A"
            }
    except:
        pass

    try:
        devices = ADLManager.getInstance().getDevices()
        for dev in devices:
            raw_name = dev.adapterName.decode('utf-8') if isinstance(dev.adapterName, bytes) else dev.adapterName
            for m_name in master_gpus:
                if raw_name in m_name or m_name in raw_name:
                    master_gpus[m_name]["load"] = float(dev.getCurrentUsage() or 0.0)
                    master_gpus[m_name]["temp"] = dev.getCurrentTemperature()
    except:
        pass

    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            for m_name in master_gpus:
                if gpu.name in m_name or m_name in gpu.name:
                    master_gpus[m_name]["load"] = gpu.load * 100
                    master_gpus[m_name]["temp"] = gpu.temperature
                    master_gpus[m_name]["memory_used"] = int(gpu.memoryUsed)
    except:
        pass

    return list(master_gpus.values())