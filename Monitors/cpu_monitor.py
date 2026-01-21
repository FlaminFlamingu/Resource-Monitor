"""CPU Monitoring Module

This module retrieves real-time CPU statistics including processor name, current load percentage,
and CPU temperature. It utilizes WMI (Windows Management Instrumentation) for detailed processor
information and thermal data, along with psutil for CPU load metrics.

Functions:
- get_cpu_stats(): Returns a dictionary containing CPU name, load percentage, and temperature
"""

import wmi
import psutil

def get_cpu_stats():
    cpu_info = {}
    try:
        w = wmi.WMI()
        for processor in w.Win32_Processor():
            cpu_info['name'] = processor.Name.strip()

        cpu_info['load'] = psutil.cpu_percent(interval=None)

        w_temp = wmi.WMI(namespace="root\\wmi")
        temp_data = w_temp.MSAcpi_ThermalZoneTemperature()
        if temp_data:
            raw_temp = temp_data[0].CurrentTemperature
            cpu_info['temp'] = (raw_temp / 10.0) - 273.15
        else:
            cpu_info['temp'] = "N/A"

    except Exception:
        cpu_info['temp'] = "N/A"
        if 'name' not in cpu_info:
            cpu_info['name'] = "Unknown Processor"
        cpu_info['load'] = psutil.cpu_percent(interval=None)

    return cpu_info