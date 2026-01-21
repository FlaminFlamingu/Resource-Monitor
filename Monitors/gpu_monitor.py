"""
FILE DESCRIPTION:
This module is responsible for detecting and monitoring dedicated Graphics 
Processing Units (GPUs). It gathers real-time data on GPU utilization, 
core temperature, and Video RAM (VRAM) usage for both NVIDIA and AMD hardware.
"""

"""
LIBRARY DESCRIPTIONS:
- GPUtil: A specialized library for retrieving NVIDIA GPU status.
- pyadl: The Python AMD Display Library, used for accessing AMD GPU metrics.
- wmi: Windows Management Instrumentation, used to identify hardware names 
       and base specifications from the system registry.
"""

import GPUtil # Interface for NVIDIA GPU monitoring
from pyadl import ADLManager # Interface for AMD GPU monitoring
import wmi # Interface for Windows system hardware identification

def get_gpu_stats():
    # Primary dictionary to store and sync data from multiple hardware sources
    master_gpus = {}

    # Identify dedicated GPUs using Windows Management Instrumentation (WMI)
    try:
        w = wmi.WMI()
        for gpu in w.Win32_VideoController():
            name = gpu.Name
            # Skip integrated Intel graphics to focus on dedicated performance
            if "Intel" in name: 
                continue
            
            # Convert VRAM from bytes to Megabytes (MB)
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

    # Gather data for AMD GPUs using the ADL library
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

    # Gather data for NVIDIA GPUs using GPUtil
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

    # Convert the dictionary of GPUs into a list for the dashboard display
    return list(master_gpus.values())