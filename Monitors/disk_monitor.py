"""
FILE: disk_monitor.py
PURPOSE: Handles storage partition detection and per-drive usage visualization.

KEY COMPONENTS:
1. DRIVE SCANNER: Identifies all fixed logical disks on the system.
2. CAPACITY ANALYZER: Calculates GB used vs. total capacity for each partition.
3. DYNAMIC UI: Generates a labeled container and progress bar for every detected drive.
"""

"""
LIBRARIES USED:
1. psutil: Disk partition and usage data provider.
2. PySide6: UI layout and styling components.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QProgressBar
from PySide6.QtCore import Qt
import psutil
import design

class StorageTab(QWidget):
    def __init__(self):
        super().__init__()
        # Main layout for the storage slide
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        
        # Initial scan and UI build
        self.refresh_storage()

    def refresh_storage(self):
        # Header for the storage analysis page
        title = QLabel("DETAILED STORAGE ANALYSIS")
        title.setStyleSheet(f"color: {design.COLORS['primary']}; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(title)

        # Iterate through all partitions (Fixed drives only)
        for part in psutil.disk_partitions():
            # Filters for physical hard drives and SSDs
            if 'fixed' in part.opts or part.fstype:
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    
                    # Create a styled container for each drive's info
                    container = QFrame()
                    container.setStyleSheet(f"background: {design.COLORS['surface']}; border-radius: 10px; margin-bottom: 15px; padding: 10px;")
                    row = QVBoxLayout(container)
                    
                    # Drive Name and Device Path
                    info = QLabel(f"Drive {part.mountpoint} ({part.device})")
                    info.setStyleSheet("font-weight: bold; color: white; font-size: 14px;")
                    
                    # Custom progress bar using the primary pink color
                    bar = QProgressBar()
                    bar.setStyleSheet(f"""
                        QProgressBar {{ 
                            border: 1px solid #333; 
                            height: 20px; 
                            border-radius: 5px; 
                            text-align: center; 
                            color: white; 
                            background: #111; 
                        }}
                        QProgressBar::chunk {{ 
                            background-color: {design.COLORS['primary']}; 
                        }}
                    """)
                    bar.setValue(int(usage.percent))
                    
                    # Text breakdown of GB usage
                    stats = QLabel(f"Used: {usage.used // (1024**3)} GB / Total: {usage.total // (1024**3)} GB")
                    stats.setStyleSheet("color: #888; font-size: 11px;")
                    
                    row.addWidget(info)
                    row.addWidget(bar)
                    row.addWidget(stats)
                    self.layout.addWidget(container)
                except Exception:
                    # Skips drives that are locked or inaccessible
                    continue