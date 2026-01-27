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

def get_usb_devices():
    # Queries the system for all currently connected USB Disk Drives.
    # Returns a dictionary mapping SerialNumber to Model Name.
    try:
        c = wmi.WMI()
        # We create a dictionary so we can show the USER-FRIENDLY name (Model)
        # while using the SerialNumber as the unique ID.
        return {d.SerialNumber.strip(): d.Model for d in c.Win32_DiskDrive() if d.InterfaceType == "USB"}
    except Exception:
        return {}

def check_usb_updates(previous_snapshot):
    """
    Compares the current system state against the previous snapshot.
    Returns:
    - current_snapshot: The new list of devices
    - added: Names of newly connected drives
    - removed: Names of disconnected drives
    """
    current_snapshot = get_usb_devices()
    
    # Set math to find the difference in Serial Numbers
    added_serials = set(current_snapshot.keys()) - set(previous_snapshot.keys())
    removed_serials = set(previous_snapshot.keys()) - set(current_snapshot.keys())
    
    # Get the human-readable names for the changes
    added_names = [current_snapshot[s] for s in added_serials]
    removed_names = [previous_snapshot[s] for s in removed_serials]
    
    return current_snapshot, added_names, removed_names