"""
FILE DESCRIPTION:
This module is responsible for detecting and monitoring Graphics 
Processing Units (GPUs). It is optimized for laptops to detect both 
Integrated (iGPU) and Dedicated (dGPU) hardware, ensuring thermal 
and load data is gathered for all active graphics controllers.
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
try:
    from pyadl import ADLManager
    AMD_DRIVER_FOUND = True
except Exception:
    AMD_DRIVER_FOUND = False

def get_gpu_stats():
    # Primary dictionary to store and sync data from multiple hardware sources
    master_gpus = {}

    # --- SECTION 1: HARDWARE IDENTIFICATION (WMI) ---
    try:
        w = wmi.WMI()
        for gpu in w.Win32_VideoController():
            name = gpu.Name
            
            # Identify if the card is Integrated or Dedicated
            # Most laptops use Intel or AMD Radeon Graphics for integrated chips
            is_integrated = any(term in name for term in ["Intel", "Integrated", "UHD", "Iris"])
            gpu_type = " (iGPU)" if is_integrated else " (dGPU)"
            
            # Convert VRAM from bytes to Megabytes (MB)
            vram_mb = abs(int(int(gpu.AdapterRAM or 0) / (1024**2)))
            
            master_gpus[name] = {
                "name": name + gpu_type, # Labeling the type for the UI
                "load": 0.0,
                "memory_total": vram_mb,
                "memory_used": "N/A",
                "temp": "N/A",
                "is_integrated": is_integrated
            }
    except Exception:
        pass

    # --- SECTION 2: AMD PERFORMANCE DATA ---
    if AMD_DRIVER_FOUND:
        try:
            devices = ADLManager.getInstance().getDevices()
            for dev in devices:
                raw_name = dev.adapterName.decode('utf-8') if isinstance(dev.adapterName, bytes) else dev.adapterName
                for m_name in master_gpus:
                    if raw_name in m_name or m_name in raw_name:
                        master_gpus[m_name]["load"] = float(dev.getCurrentUsage() or 0.0)
                        master_gpus[m_name]["temp"] = dev.getCurrentTemperature()
        except Exception:
            pass

    # --- SECTION 3: NVIDIA PERFORMANCE DATA ---
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            for m_name in master_gpus:
                # NVIDIA cards are almost always dedicated (dGPU)
                if gpu.name in m_name or m_name in gpu.name:
                    master_gpus[m_name]["load"] = gpu.load * 100
                    master_gpus[m_name]["temp"] = gpu.temperature
                    master_gpus[m_name]["memory_used"] = int(gpu.memoryUsed)
    except Exception:
        pass

    return list(master_gpus.values())