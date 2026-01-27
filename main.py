"""
FILE DESCRIPTION:
This is the main execution engine of the System Monitor. It manages 
the synchronization between the specialized hardware monitors and 
the dashboard UI, specifically handling the separation of fixed 
disk data (Yellow) and USB hot-plug alerts (Orange).
"""

"""
PROJECT MODULE IMPORTS:
- design: Renders the ASCII dashboard with Yellow and Orange sections.
- Monitors: A package containing the CPU, GPU, Memory, Disk, and USB 
  collection logic.
"""

"""
LIBRARY DESCRIPTIONS:
- time: Handles the 1-second refresh rate of the dashboard.
- sys: Manages the clean exit of the Python runtime.
"""

import time # Library for controlling loop speed
import sys  # Library for clean system exits

# Project modules for UI and Data Collection
from design import draw_dashboard, B_RED, RESET
from Monitors import cpu_monitor, gpu_monitor, memory_monitor, disk_monitor, usb_monitor

def start():
    # Initialize the USB state and the notification log before starting the loop
    last_usb_state = usb_monitor.get_usb_devices()
    usb_log = ["No recent activity"] # Default message for the Orange UI box

    try:
        while True:
            # Gathers real-time statistics (Internal Disks are filtered in disk_monitor)
            cpu_data = cpu_monitor.get_cpu_stats()       
            gpu_data = gpu_monitor.get_gpu_stats()       
            mem_data = memory_monitor.get_memory_stats() 
            disk_data = disk_monitor.get_disk_stats()    

            # Polling for USB changes to populate the Orange alert box
            current_usb, newly_added, newly_removed = usb_monitor.check_usb_updates(last_usb_state)
            
            if newly_added:
                if "No recent activity" in usb_log: usb_log.clear()
                usb_log.append(f"DETECTED: {list(newly_added)[0]}")
            
            if newly_removed:
                if "No recent activity" in usb_log: usb_log.clear()
                usb_log.append(f"REMOVED: {list(newly_removed)[0]}")

            # Keep only the 3 most recent hardware events
            usb_log = usb_log[-3:]
            last_usb_state = current_usb

            # Pass all data to the dashboard, including the separate USB log
            draw_dashboard(cpu_data, gpu_data, mem_data, disk_data, usb_log)

            # Wait 1 second before the next UI refresh
            time.sleep(1)

    except KeyboardInterrupt:
        # Professional exit message on Ctrl+C
        print(f"\n{B_RED}Monitoring Stopped!{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    start()