"""
FILE DESCRIPTION:
This module retrieves real-time CPU statistics. It captures the 
official processor name, monitors the current usage load as a 
percentage, and attempts to pull thermal data to track the CPU temperature.
"""

"""
LIBRARY DESCRIPTIONS:
- wmi: Windows Management Instrumentation is used to access deep system 
       information like the processor's hardware name and thermal zone sensors.
- psutil: A library used here to calculate the current CPU utilization 
          load across all logical cores.
"""

import wmi # Library for accessing Windows-specific system and sensor data
import psutil # Library for retrieving system-wide CPU utilization percentages

def get_cpu_stats():
    # Dictionary to store the gathered CPU attributes
    cpu_info = {}
    try:
        # Connect to WMI to get the processor's hardware name
        w = wmi.WMI()
        for processor in w.Win32_Processor():
            cpu_info['name'] = processor.Name.strip()

        # Get the current CPU load (non-blocking interval for real-time updates)
        cpu_info['load'] = psutil.cpu_percent(interval=None)

        # Access the WMI thermal namespace to read temperature sensors
        w_temp = wmi.WMI(namespace="root\\wmi")
        temp_data = w_temp.MSAcpi_ThermalZoneTemperature()
        
        if temp_data:
            # WMI returns temperature in tenths of Kelvins; converting to Celsius
            raw_temp = temp_data[0].CurrentTemperature
            cpu_info['temp'] = round((raw_temp / 10.0) - 273.15, 1)
        else:
            cpu_info['temp'] = "N/A"

    except Exception:
        # Fallback values in case of permission issues or missing sensors
        cpu_info['temp'] = "N/A"
        if 'name' not in cpu_info:
            cpu_info['name'] = "Unknown Processor"
        cpu_info['load'] = psutil.cpu_percent(interval=None)

    return cpu_info