"""
FILE: main.py
PURPOSE: Multi-tab hardware monitor with specialized slides for CPU, RAM, Storage, and GPU.

KEY COMPONENTS:
1. TASKBAR OVERRIDE: Uses 'flaminflamingu.resource.monitor' ID for unique taskbar grouping.
2. DYNAMIC SLIDES: Dedicated classes for CPU (per-core), RAM (allocation), Storage (per-drive), and GPU.
3. BRANDING: Global application of 'assets/logo.png' to window and taskbar.
"""

"""
LIBRARIES USED:
1. psutil: Core system metrics engine.
2. PySide6: GUI framework and styling engine.
3. ctypes: Windows shell integration.
4. GPUtil: NVIDIA hardware monitoring.
"""

import sys
import os
import psutil
import ctypes
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QGridLayout, QFrame, QLabel, QProgressBar, QScrollArea)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, Qt
import design 

# Windows Taskbar Branding Fix
try:
    my_app_id = 'flaminflamingu.resource.monitor' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
except Exception:
    pass

try:
    import GPUtil
    HAS_GPU = True
except ImportError:
    HAS_GPU = False

class MetricCard(QFrame):
    # Reusable card component for the Dashboard
    def __init__(self, title, start_val):
        super().__init__()
        self.setFixedSize(400, 220)
        self.setStyleSheet(f"QFrame {{ background-color: {design.COLORS['surface']}; border: 2px solid {design.COLORS['primary']}; border-radius: 20px; padding: 20px; }}")
        layout = QVBoxLayout(self)
        self.t_label = QLabel(title)
        self.t_label.setStyleSheet("color: #888888; font-size: 12px; border: none; font-weight: bold;")
        self.value_label = QLabel(start_val)
        self.value_label.setStyleSheet(f"color: {design.COLORS['text']}; font-size: 48px; font-weight: 600; border: none;")
        layout.addWidget(self.t_label)
        layout.addStretch() 
        layout.addWidget(self.value_label, alignment=Qt.AlignCenter)

class DashboardTab(QWidget):
    # Main overview slide with metric cards
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        main_layout.setContentsMargins(0, 40, 0, 30)

        brand = QLabel(design.APP_NAME)
        brand.setStyleSheet(f"font-size: 72px; font-weight: bold; color: {design.COLORS['primary']};")
        main_layout.addWidget(brand, alignment=Qt.AlignCenter)

        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        self.cpu_card = MetricCard("🖥️ CPU USAGE", "0%")
        self.ram_card = MetricCard("🧠 RAM STATUS", "0%")
        self.disk_card = MetricCard("💾 STORAGE (TOTAL)", "0%")
        self.gpu_card = MetricCard("🎮 GPU LOAD", "N/A")
        grid.addWidget(self.cpu_card, 0, 0); grid.addWidget(self.ram_card, 0, 1)
        grid.addWidget(self.disk_card, 1, 0); grid.addWidget(self.gpu_card, 1, 1)
        main_layout.addWidget(grid_container, alignment=Qt.AlignCenter)

    def update_metrics(self):
        self.cpu_card.value_label.setText(f"{psutil.cpu_percent()}%")
        self.ram_card.value_label.setText(f"{psutil.virtual_memory().percent}%")
        t_used = sum(psutil.disk_usage(p.mountpoint).used for p in psutil.disk_partitions() if 'fixed' in p.opts)
        t_total = sum(psutil.disk_usage(p.mountpoint).total for p in psutil.disk_partitions() if 'fixed' in p.opts)
        self.disk_card.value_label.setText(f"{(t_used/t_total)*100:.1f}%" if t_total > 0 else "0%")
        if HAS_GPU:
            gpus = GPUtil.getGPUs()
            self.gpu_card.value_label.setText(f"{gpus[0].load*100:.1f}%" if gpus else "N/A")

class CPUTab(QWidget):
    # Detailed slide for individual CPU cores
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        title = QLabel("CPU CORE ANALYSIS")
        title.setStyleSheet(f"color: {design.COLORS['primary']}; font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(title)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)
        self.core_bars = []
        self.setup_cores()

    def setup_cores(self):
        cores = psutil.cpu_percent(percpu=True)
        for i, usage in enumerate(cores):
            label = QLabel(f"CORE {i}")
            label.setStyleSheet("color: white; font-weight: bold;")
            bar = QProgressBar()
            bar.setStyleSheet(f"QProgressBar {{ border: 1px solid #333; border-radius: 5px; text-align: center; color: white; background: #111; }} QProgressBar::chunk {{ background-color: {design.COLORS['primary']}; }}")
            bar.setValue(int(usage))
            self.grid.addWidget(label, i, 0)
            self.grid.addWidget(bar, i, 1)
            self.core_bars.append(bar)

    def update_cpu_details(self):
        cores = psutil.cpu_percent(percpu=True)
        for i, usage in enumerate(cores):
            if i < len(self.core_bars):
                self.core_bars[i].setValue(int(usage))

class RAMTab(QWidget):
    # Detailed slide for Memory and Swap
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("MEMORY ALLOCATION")
        title.setStyleSheet(f"color: {design.COLORS['primary']}; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)
        self.ram_bar = QProgressBar()
        self.ram_bar.setStyleSheet(f"QProgressBar {{ border: 1px solid #333; height: 30px; border-radius: 5px; text-align: center; color: white; background: #111; }} QProgressBar::chunk {{ background-color: {design.COLORS['primary']}; }}")
        self.details = QLabel("Loading RAM metrics...")
        self.details.setStyleSheet("color: white; font-size: 14px; margin-top: 10px;")
        layout.addWidget(QLabel("Physical Memory (RAM)"))
        layout.addWidget(self.ram_bar)
        layout.addWidget(self.details)
        layout.addStretch()

    def update_ram(self):
        mem = psutil.virtual_memory()
        self.ram_bar.setValue(int(mem.percent))
        self.details.setText(f"Used: {mem.used // (1024**2)}MB / Total: {mem.total // (1024**2)}MB\nAvailable: {mem.available // (1024**2)}MB")

class StorageTab(QWidget):
    # Detailed slide for individual drives
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
                    container.setStyleSheet(f"background: {design.COLORS['surface']}; border-radius: 10px; margin-bottom: 10px;")
                    row = QVBoxLayout(container)
                    info = QLabel(f"Drive {part.mountpoint} ({part.device})")
                    info.setStyleSheet("font-weight: bold; color: white;")
                    bar = QProgressBar()
                    bar.setStyleSheet(f"QProgressBar {{ border: 1px solid #333; border-radius: 5px; text-align: center; color: white; background: #111; }} QProgressBar::chunk {{ background-color: {design.COLORS['primary']}; }}")
                    bar.setValue(int(usage.percent))
                    stats = QLabel(f"Used: {usage.used // (1024**3)}GB / Total: {usage.total // (1024**3)}GB")
                    stats.setStyleSheet("color: #888; font-size: 11px;")
                    row.addWidget(info); row.addWidget(bar); row.addWidget(stats)
                    self.layout.addWidget(container)
                except: continue

class GPUTab(QWidget):
    # Detailed slide for GPU statistics
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.title = QLabel("GPU HARDWARE ANALYSIS")
        self.title.setStyleSheet(f"color: {design.COLORS['primary']}; font-size: 24px; font-weight: bold;")
        layout.addWidget(self.title)
        self.info = QLabel("Detecting GPU...")
        self.info.setStyleSheet("color: white; font-size: 16px; margin-top: 20px;")
        layout.addWidget(self.info)
        layout.addStretch()

    def update_gpu(self):
        if HAS_GPU:
            gpus = GPUtil.getGPUs()
            if gpus:
                g = gpus[0]
                self.info.setText(f"Name: {g.name}\nLoad: {g.load*100:.1f}%\nTemp: {g.temperature} C\nMemory: {g.memoryUsed}MB / {g.memoryTotal}MB")
            else:
                self.info.setText("No active GPU load detected.")
        else:
            self.info.setText("GPUtil not found or No NVIDIA GPU detected.")

class FlaminProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlaminFlamingu")
        self.resize(1200, 900)
        self.apply_icon()
        self.setStyleSheet(design.get_main_style())
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Initialize all slides
        self.dashboard = DashboardTab()
        self.cpu_slide = CPUTab()
        self.ram_slide = RAMTab()
        self.storage_slide = StorageTab()
        self.gpu_slide = GPUTab()
        
        # Add Tabs
        self.tabs.addTab(self.dashboard, "📊 DASHBOARD")
        self.tabs.addTab(self.cpu_slide, "🖥️ CPU")
        self.tabs.addTab(self.ram_slide, "🧠 RAM")
        self.tabs.addTab(self.storage_slide, "💾 STORAGE")
        self.tabs.addTab(self.gpu_slide, "🎮 GPU")
        
        # Global Update Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.dashboard.update_metrics)
        self.timer.timeout.connect(self.cpu_slide.update_cpu_details)
        self.timer.timeout.connect(self.ram_slide.update_ram)
        self.timer.timeout.connect(self.gpu_slide.update_gpu)
        self.timer.start(1000)

    def apply_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            self.setWindowIcon(app_icon)
            QApplication.setWindowIcon(app_icon)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlaminProApp()
    window.show()
    sys.exit(app.exec())