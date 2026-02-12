"""
FILE DESCRIPTION:
This module is responsible for detecting and monitoring dedicated Graphics 
Processing Units (GPUs). It gathers real-time data on GPU utilization, 
core temperature, and Video RAM (VRAM) usage for both NVIDIA and AMD hardware.
By using 'lazy imports' and driver checks, the script prevents crashes on 
systems where specific drivers (like AMD ADL) are missing.
"""

"""
LIBRARY DESCRIPTIONS:
- GPUtil: Used for NVIDIA cards. Note: Requires 'setuptools' on Python 3.12+.
- pyadl: The Python AMD Display Library, used for accessing AMD GPU metrics.
- wmi: Windows Management Instrumentation, used to identify hardware names 
        and base specifications from the system registry.
"""

# BACKGROUND DEPENDENCY: setuptools (Required for GPUtil compatibility on Python 3.12+)
import GPUtil  # Interface for NVIDIA GPU monitoring
import wmi     # Interface for Windows system hardware identification

# --- DRIVER VALIDATION ---
# Attempt to import the AMD library. If the driver is missing, the program 
# sets a flag to False instead of crashing the entire application.
try:
    from pyadl import ADLManager
    AMD_DRIVER_FOUND = True
except Exception:
    AMD_DRIVER_FOUND = False

def get_gpu_stats():
    # Primary dictionary to store and sync data from multiple hardware sources
    master_gpus = {}

    # --- SECTION 1: HARDWARE IDENTIFICATION (WMI) ---
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
    except Exception:
        pass

    # --- SECTION 2: AMD PERFORMANCE DATA ---
    # Only executes if the AMD Display Library (ADL) was successfully loaded.
    if AMD_DRIVER_FOUND:
        try:
            devices = ADLManager.getInstance().getDevices()
            for dev in devices:
                # Handle potential byte-string naming from old AMD drivers
                raw_name = dev.adapterName.decode('utf-8') if isinstance(dev.adapterName, bytes) else dev.adapterName
                for m_name in master_gpus:
                    if raw_name in m_name or m_name in raw_name:
                        master_gpus[m_name]["load"] = float(dev.getCurrentUsage() or 0.0)
                        master_gpus[m_name]["temp"] = dev.getCurrentTemperature()
        except Exception:
            pass

    # --- SECTION 3: NVIDIA PERFORMANCE DATA ---
    # Gather data for NVIDIA GPUs using GPUtil
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            for m_name in master_gpus:
                if gpu.name in m_name or m_name in gpu.name:
                    # Convert load to percentage and store temperature/memory
                    master_gpus[m_name]["load"] = gpu.load * 100
                    master_gpus[m_name]["temp"] = gpu.temperature
                    master_gpus[m_name]["memory_used"] = int(gpu.memoryUsed)
    except Exception:
        pass

    # Convert the dictionary of GPUs into a list for the dashboard display
    return list(master_gpus.values())