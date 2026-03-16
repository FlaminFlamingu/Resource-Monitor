"""
FILE: disk_monitor.py
PURPOSE: Handles storage partition detection and visualization.
"""

import sys
import os
import psutil
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QProgressBar
from PySide6.QtCore import Qt

# Path Fix: Allows this script to see design.py in the root folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import design

class StorageTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.refresh_storage()

    def refresh_storage(self):
        title = QLabel("DETAILED STORAGE ANALYSIS")
        title.setStyleSheet(f"color: {design.COLORS['primary']}; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(title)

        for part in psutil.disk_partitions():
            if 'fixed' in part.opts or part.fstype:
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    container = QFrame()
                    container.setStyleSheet(f"background: {design.COLORS['surface']}; border-radius: 10px; margin-bottom: 15px; padding: 10px;")
                    row = QVBoxLayout(container)
                    
                    info = QLabel(f"Drive {part.mountpoint}")
                    info.setStyleSheet("font-weight: bold; color: white;")
                    
                    bar = QProgressBar()
                    bar.setStyleSheet(f"QProgressBar {{ border: 1px solid #333; height: 20px; border-radius: 5px; text-align: center; color: white; background: #111; }} QProgressBar::chunk {{ background-color: {design.COLORS['primary']}; }}")
                    bar.setValue(int(usage.percent))
                    
                    row.addWidget(info)
                    row.addWidget(bar)
                    self.layout.addWidget(container)
                except: continue