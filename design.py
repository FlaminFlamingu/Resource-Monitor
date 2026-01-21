"""
FILE DESCRIPTION:
This script handles the User Interface (UI) design for the System Monitor. 
It defines how the hardware data is visually structured using ASCII 
border characters and organized into clear, color-coded sections.
"""

"""
COLOR PALETTE AVAILABILITY:
This module contains a full suite of standard and bright ANSI color codes.
These variables can be used to customize the text color of any dashboard 
element by wrapping the string in the desired color variable.
"""

"""
LIBRARY DESCRIPTIONS:
- os: Used for initializing the terminal's color support and 
      clearing the screen to create a static dashboard effect.
"""

import os # Library used for clearing the screen and enabling ANSI colors

# Initialize terminal for ANSI color support
os.system("")

# Standard Colors
BLACK     = '\033[30m'
RED       = '\033[31m'
GREEN     = '\033[32m'
YELLOW    = '\033[33m'
BLUE      = '\033[34m'
MAGENTA   = '\033[35m'
CYAN      = '\033[36m'
WHITE     = '\033[37m'

# Bright/Bold Colors
B_BLACK   = '\033[90m'
B_RED     = '\033[91m'
B_GREEN   = '\033[92m'
B_YELLOW  = '\033[93m'
B_BLUE    = '\033[94m'
B_MAGENTA = '\033[95m'
B_CYAN    = '\033[96m'
B_WHITE   = '\033[97m'

RESET     = '\033[0m'

def clear_screen():
    # Detects the operating system and runs the correct command to clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_dashboard(cpu, gpus, mem, disks):
    # Main function to render the UI components with live data
    clear_screen()
    
    W = 50 # Fixed width used for horizontal alignment of the ASCII boxes

    # Header Box (Cyan)
    print(f"{B_CYAN}┌──────────────────────────────────────────────────┐")
    print(f"│             SYSTEM RESOURCE MONITOR              │")
    print(f"└──────────────────────────────────────────────────┘{RESET}")
    
    # Stop Info (Red text positioned directly below the header)
    print(f"{B_RED}               Press Ctrl+C to Stop               {RESET}")

    # CPU Section (Blue) - Shows processor name and real-time load/temp
    print(f"\n{B_BLUE}┌── CPU {'─' * 43}┐")
    print(f"│{f' Name: {cpu['name'][:40]}':<{W}}│")
    print(f"│{f' Load: {cpu['load']}%':<{W}}│")
    print(f"│{f' Temp: {cpu['temp']}C':<{W}}│")
    print(f"└──────────────────────────────────────────────────┘{RESET}")

    # GPU Section (Magenta) - Loops through each available graphics card
    for gpu in gpus:
        print(f"\n{B_MAGENTA}┌── GPU {'─' * 43}┐")
        print(f"│{f' Name: {gpu['name']}':<{W}}│")
        print(f"│{f' Load: {gpu['load']}%':<{W}}│")
        print(f"│{f' Temp: {gpu['temp']}C':<{W}}│")
        print(f"│{f' VRAM: {gpu['memory_used']} / {gpu['memory_total']}MB':<{W}}│")
        print(f"└──────────────────────────────────────────────────┘{RESET}")

    # Memory Section (Green) - Displays RAM percentage and total GB stats
    print(f"\n{B_GREEN}┌── MEMORY {'─' * 40}┐")
    print(f"│{f' Used: {mem['percent']}%':<{W}}│")
    print(f"│{f' Stats: {mem['used']}GB / {mem['total']}GB':<{W}}│")
    print(f"└──────────────────────────────────────────────────┘{RESET}")

    # Storage Section (Yellow) - Displays disk device names and usage percentages
    print(f"\n{B_YELLOW}┌── STORAGE {'─' * 39}┐")
    for disk in disks:
        d_text = f" {disk['device']} ({disk['mount']}): {disk['percent']}% Used"
        print(f"│{f'{d_text}':<{W}}│")
    print(f"└──────────────────────────────────────────────────┘{RESET}")