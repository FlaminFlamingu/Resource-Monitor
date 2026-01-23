"""
FILE DESCRIPTION:
This module handles USB detection through polling. It compares the current 
list of physical drives against a previous snapshot to identify when a 
new device has been plugged in or removed.
"""

"""
LIBRARY DESCRIPTIONS:
- wmi: Used to query the Win32_DiskDrive class to get physical hardware 
       names and interface types (USB vs IDE/SCSI).
"""

import wmi # Library for querying physical hardware properties

def get_physical_disks():
    # Returns a set of unique serial numbers or device IDs currently plugged in
    try:
        c = wmi.WMI()
        # We look specifically for USB interface types
        return {d.SerialNumber.strip() for d in c.Win32_DiskDrive() if d.InterfaceType == "USB"}
    except:
        return set()

def check_for_new_usb(previous_snapshot):
    # Compares the new list of USBs to the old one
    current_snapshot = get_physical_disks()
    
    # Identify new additions
    new_devices = current_snapshot - previous_snapshot
    
    # Identify removals
    removed_devices = previous_snapshot - current_snapshot
    
    return current_snapshot, new_devices, removed_devices