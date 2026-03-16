"""
FILE: main.py
PURPOSE: Central GUI Manager and Dashboard for the FlaminFlamingu Resource Monitor.

KEY COMPONENTS:
1. DASHBOARD ENGINE: Internal classes for the high-level overview cards.
2. MODULAR INTEGRATION: Pulls detailed hardware slides from the /Monitors folder.
3. THEME APPLICATION: Injects the global Pink & Black QSS from design.py.
"""

"""
LIBRARIES USED:
1. PySide6: Core GUI framework and widget management.
2. psutil: System-wide resource usage data.
3. design: Consolidated branding and style engine.
"""

import sys
import os
import ctypes
import psutil
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, Qt
import design

# Import specialized detail slides from the sub-folder
from Monitors import cpu_monitor, memory_monitor, disk_monitor, gpu_monitor

# Attempt to load GPU library for the dashboard summary
try:
    import GPUtil
    HAS_GPU = True
except ImportError:
    HAS_GPU = False

class MetricCard(QFrame):
    # Reusable UI card for the overview dashboard
    def __init__(self, title, start_val):
        super().__init__()
        self.setFixedSize(300, 180)
        self.setStyleSheet(f"""
            QFrame {{ 
                background-color: {design.COLORS['surface']}; 
                border: 2px solid {design.COLORS['primary']}; 
                border-radius: 20px; 
                padding: 15px; 
            }}
        """)
        layout = QVBoxLayout(self)
        
        self.t_label = QLabel(title)
        self.t_label.setStyleSheet(f"color: {design.COLORS['accent']}; font-size: 12px; font-weight: bold; border: none;")
        
        self.value_label = QLabel(start_val)
        self.value_label.setStyleSheet(f"color: {design.COLORS['text']}; font-size: 42px; font-weight: 600; border: none;")
        
        layout.addWidget(self.t_label)
        layout.addStretch() 
        layout.addWidget(self.value_label, alignment=Qt.AlignCenter)

class DashboardTab(QWidget):
    # The primary landing page showing a summary of all vitals
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        main_layout.setContentsMargins(0, 40, 0, 0)

        # Main Title Branding
        header = QLabel(design.APP_NAME)
        header.setStyleSheet(f"font-size: 52px; font-weight: bold; color: {design.COLORS['primary']};")
        main_layout.addWidget(header, alignment=Qt.AlignCenter)

        # Grid for the overview cards
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        
        self.cpu_card = MetricCard("🖥️ CPU USAGE", "0%")
        self.ram_card = MetricCard("🧠 RAM STATUS", "0%")
        self.disk_card = MetricCard("💾 STORAGE", "0%")
        self.gpu_card = MetricCard("🎮 GPU LOAD", "N/A")
        
        grid.addWidget(self.cpu_card, 0, 0)
        grid.addWidget(self.ram_card, 0, 1)
        grid.addWidget(self.disk_card, 1, 0)
        grid.addWidget(self.gpu_card, 1, 1)
        
        main_layout.addWidget(grid_container, alignment=Qt.AlignCenter)

    def update_metrics(self):
        # Updates the dashboard card values
        self.cpu_card.value_label.setText(f"{psutil.cpu_percent()}%")
        self.ram_card.value_label.setText(f"{psutil.virtual_memory().percent}%")
        
        try:
            usage = psutil.disk_usage('/')
            self.disk_card.value_label.setText(f"{usage.percent}%")
        except:
            self.disk_card.value_label.setText("N/A")

        if HAS_GPU:
            gpus = GPUtil.getGPUs()
            self.gpu_card.value_label.setText(f"{gpus[0].load*100:.0f}%" if gpus else "N/A")

class FlaminProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(design.APP_NAME)
        self.resize(1200, 900)
        
        # Windows Taskbar Branding Fix
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('flaminflamingu.monitor')
        except: pass

        self.apply_icon()
        self.setStyleSheet(design.get_main_style())
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Initialize internal dashboard and external modular slides
        self.dashboard = DashboardTab()
        self.cpu_slide = cpu_monitor.CPUTab()
        self.ram_slide = memory_monitor.RAMTab()
        self.storage_slide = disk_monitor.StorageTab()
        self.gpu_slide = gpu_monitor.GPUTab()
        
        self.tabs.addTab(self.dashboard, "📊 DASHBOARD")
        self.tabs.addTab(self.cpu_slide, "🖥️ CPU")
        self.tabs.addTab(self.ram_slide, "🧠 RAM")
        self.tabs.addTab(self.storage_slide, "💾 STORAGE")
        self.tabs.addTab(self.gpu_slide, "🎮 GPU")
        
        # Centralized 1s timer for all updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.dashboard.update_metrics)
        self.timer.timeout.connect(self.cpu_slide.update_cpu_details)
        self.timer.timeout.connect(self.ram_slide.update_ram)
        self.timer.timeout.connect(self.gpu_slide.update_gpu)
        self.timer.start(1000)

    def apply_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            self.setWindowIcon(app_icon)
            QApplication.setWindowIcon(app_icon)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlaminProApp()
    window.show()
    sys.exit(app.exec())