"""Dashboard Design and Color Configuration Module

This module defines the visual presentation and layout of the System Resource Monitor dashboard.
It provides ANSI color definitions for terminal output and the main dashboard rendering function
that displays system resource information in an organized, color-coded format.

Features:
- Standard and bright ANSI color definitions
- Dashboard layout with organized sections for CPU, GPU, Memory, and Disk information
- Screen clearing functionality compatible with Windows and Unix systems
"""

import os

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
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_dashboard(cpu, gpus, mem, disks):
    clear_screen()
    
    W = 50 

    # Header Box (Cyan)
    print(f"{B_CYAN}┌──────────────────────────────────────────────────┐")
    print(f"│             SYSTEM RESOURCE MONITOR              │")
    print(f"└──────────────────────────────────────────────────┘{RESET}")
    
    # Stop Info (Red, No punctuation at the end as requested)
    print(f"{B_RED}               Press Ctrl+C to Stop               {RESET}")

    # CPU Section
    print(f"\n{B_BLUE}┌── CPU {'─' * 43}┐")
    print(f"│{f' Name: {cpu['name'][:40]}':<{W}}│")
    print(f"│{f' Load: {cpu['load']}%':<{W}}│")
    print(f"│{f' Temp: {cpu['temp']}C':<{W}}│")
    print(f"└──────────────────────────────────────────────────┘{RESET}")

    # GPU Section
    for gpu in gpus:
        print(f"\n{B_MAGENTA}┌── GPU {'─' * 43}┐")
        print(f"│{f' Name: {gpu['name']}':<{W}}│")
        print(f"│{f' Load: {gpu['load']}%':<{W}}│")
        print(f"│{f' Temp: {gpu['temp']}C':<{W}}│")
        print(f"│{f' VRAM: {gpu['memory_used']} / {gpu['memory_total']}MB':<{W}}│")
        print(f"└──────────────────────────────────────────────────┘{RESET}")

    # Memory Section
    print(f"\n{B_GREEN}┌── MEMORY {'─' * 40}┐")
    print(f"│{f' Used: {mem['percent']}%':<{W}}│")
    print(f"│{f' Stats: {mem['used']}GB / {mem['total']}GB':<{W}}│")
    print(f"└──────────────────────────────────────────────────┘{RESET}")

    # Storage Section
    print(f"\n{B_YELLOW}┌── STORAGE {'─' * 39}┐")
    for disk in disks:
        d_text = f" {disk['device']} ({disk['mount']}): {disk['percent']}% Used"
        print(f"│{f'{d_text}':<{W}}│")
    print(f"└──────────────────────────────────────────────────┘{RESET}")

