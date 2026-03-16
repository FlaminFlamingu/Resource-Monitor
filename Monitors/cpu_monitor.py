"""
FILE: cpu_monitor.py
PURPOSE: Modular component for tracking per-core processor utilization.

KEY COMPONENTS:
1. CORE-LEVEL METRICS: Fetches real-time usage for every logical processor.
2. DYNAMIC UI GENERATION: Automatically scales the number of progress bars.
3. SCROLLABLE CONTAINER: Handles high-core-count CPUs.
"""

"""
LIBRARIES USED:
1. psutil: CPU metric collection.
2. PySide6: UI layout and styling.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QProgressBar, QScrollArea
from PySide6.QtCore import Qt
import psutil
import design

# The class name MUST be CPUTab for main.py to find it
class CPUTab(QWidget):
    def __init__(self):
        super().__init__()
        # Main layout for the CPU slide
        self.layout = QVBoxLayout(self)
        
        # Section Header
        title = QLabel("CPU CORE ANALYSIS")
        title.setStyleSheet(f"color: {design.COLORS['primary']}; font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(title)

        # Scroll area setup
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)

        # List to keep track of progress bar objects
        self.core_bars = []
        self.setup_cores()

    def setup_cores(self):
        # Create bars for every core
        cores = psutil.cpu_percent(percpu=True)
        for i, usage in enumerate(cores):
            label = QLabel(f"CORE {i}")
            label.setStyleSheet("color: white; font-weight: bold;")
            
            bar = QProgressBar()
            bar.setStyleSheet(f"""
                QProgressBar {{ 
                    border: 1px solid #333; 
                    border-radius: 5px; 
                    text-align: center; 
                    color: white; 
                    background: #111; 
                }}
                QProgressBar::chunk {{ 
                    background-color: {design.COLORS['primary']}; 
                }}
            """)
            bar.setValue(int(usage))
            
            self.grid.addWidget(label, i, 0)
            self.grid.addWidget(bar, i, 1)
            self.core_bars.append(bar)

    def update_cpu_details(self):
        # Polled by main.py every 1000ms
        cores = psutil.cpu_percent(percpu=True)
        for i, usage in enumerate(cores):
            if i < len(self.core_bars):
                self.core_bars[i].setValue(int(usage))