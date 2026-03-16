"""
FILE: memory_monitor.py
PURPOSE: Handles physical RAM and virtual swap memory tracking.

KEY COMPONENTS:
1. REAL-TIME ALLOCATION: Tracks how many MB of RAM are currently in use.
2. PERCENTAGE TRACKING: Calculates total memory load for the system.
3. DETAILED BREAKDOWN: Displays available vs. total physical capacity.
"""

"""
LIBRARIES USED:
1. psutil: Primary system memory metric collection.
2. PySide6: UI components for bars and labels.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
import psutil
import design

class RAMTab(QWidget):
    def __init__(self):
        super().__init__()
        # Main layout for the memory slide
        self.layout = QVBoxLayout(self)
        
        # Section Header
        title = QLabel("MEMORY ALLOCATION")
        title.setStyleSheet(f"color: {design.COLORS['primary']}; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(title)

        # Container for Physical RAM statistics
        self.container = QFrame()
        self.container.setStyleSheet(f"background: {design.COLORS['surface']}; border-radius: 15px; padding: 20px;")
        self.c_layout = QVBoxLayout(self.container)
        
        self.label = QLabel("Physical Memory (RAM)")
        self.label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        
        # Professional pink progress bar for RAM load
        self.ram_bar = QProgressBar()
        self.ram_bar.setStyleSheet(f"""
            QProgressBar {{ 
                border: 1px solid #333; 
                height: 30px; 
                border-radius: 5px; 
                text-align: center; 
                color: white; 
                background: #111; 
            }}
            QProgressBar::chunk {{ 
                background-color: {design.COLORS['primary']}; 
            }}
        """)
        
        self.details = QLabel("Loading RAM metrics...")
        self.details.setStyleSheet("color: #AAA; font-size: 14px; margin-top: 10px;")
        
        self.c_layout.addWidget(self.label)
        self.c_layout.addWidget(self.ram_bar)
        self.c_layout.addWidget(self.details)
        
        self.layout.addWidget(self.container)
        self.layout.addStretch()

    def update_ram(self):
        # This method is called by the timer in main.py
        mem = psutil.virtual_memory()
        
        # Update the progress bar percentage
        self.ram_bar.setValue(int(mem.percent))
        
        # Convert bytes to Megabytes (MB) for easier reading
        used_mb = mem.used // (1024**2)
        total_mb = mem.total // (1024**2)
        avail_mb = mem.available // (1024**2)
        
        self.details.setText(
            f"Used: {used_mb} MB / Total: {total_mb} MB\n"
            f"Available: {avail_mb} MB"
        )