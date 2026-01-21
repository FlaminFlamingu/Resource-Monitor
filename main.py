"""
FILE DESCRIPTION:
This is the main execution engine of the System Monitor. 
It acts as the 'brain' that connects the data collectors (Monitors) 
to the visual display (Design). It handles the timing loop, 
manages the exit process, and ensures errors don't crash the program.
"""

"""
LIBRARY DESCRIPTIONS:
- time: Provides functions for handling pauses (sleep) so the script doesn't overload the CPU.
- sys: Allows the script to interact with the Python runtime (used here for clean exits).
- os: Used for interacting with the operating system (clearing the terminal).
"""

import time # Library for controlling loop speed and delays
import sys  # Library for system-specific parameters and functions
import os   # Library for OS-dependent functionality

# Project modules for UI and Data Collection
from design import draw_dashboard, B_RED, RESET
from Monitors import cpu_monitor, gpu_monitor, memory_monitor, disk_monitor

def start():
    # Main execution function that gathers hardware data and updates the display.
    try:
        while True:
            # Gathers real-time statistics from each hardware component
            cpu_data = cpu_monitor.get_cpu_stats()       
            gpu_data = gpu_monitor.get_gpu_stats()       
            mem_data = memory_monitor.get_memory_stats() 
            disk_data = disk_monitor.get_disk_stats()    

            # Updates the terminal UI using the data collected above
            draw_dashboard(cpu_data, gpu_data, mem_data, disk_data)

            # Pause for 1 second before next update
            time.sleep(1)

    except KeyboardInterrupt:
        # Catch Ctrl+C and print red exit message
        print(f"\n{B_RED}Monitoring Stopped!{RESET}")
        sys.exit(0)
        
    except Exception as e:
        # Catches any unexpected errors and displays them before pausing
        print(f"System Error: {e}")
        time.sleep(2)

if __name__ == "__main__":
    start()