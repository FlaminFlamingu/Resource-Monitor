"""
FILE: memory_monitor.py
PURPOSE: Modular component for tracking RAM and swap memory.

KEY COMPONENTS:
1. PATH RESOLUTION: Appends parent directory to sys.path to access design.py.
2. RAMTab CLASS: UI component for memory visualization.
"""

"""
LIBRARIES USED:
1. psutil: Memory metric collection.
2. PySide6: UI layout.
"""

import sys
import os
import psutil
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame

# Path Fix: Allows this script to see design.py in the root folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import design

class RAMTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        title = QLabel("MEMORY ALLOCATION")
        title.setStyleSheet(f"color: {design.COLORS['primary']}; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(title)

        self.ram_bar = QProgressBar()
        self.ram_bar.setStyleSheet(f"QProgressBar {{ border: 1px solid #333; height: 30px; border-radius: 5px; text-align: center; color: white; background: #111; }} QProgressBar::chunk {{ background-color: {design.COLORS['primary']}; }}")
        
        self.details = QLabel("Loading RAM metrics...")
        self.details.setStyleSheet("color: #AAA; font-size: 14px; margin-top: 10px;")
        
        self.layout.addWidget(QLabel("Physical Memory (RAM)"))
        self.layout.addWidget(self.ram_bar)
        self.layout.addWidget(self.details)
        self.layout.addStretch()

    def update_ram(self):
        mem = psutil.virtual_memory()
        self.ram_bar.setValue(int(mem.percent))
        used_gb = mem.used // (1024**3)
        total_gb = mem.total // (1024**3)
        self.details.setText(f"Used: {used_gb} GB / Total: {total_gb} GB")