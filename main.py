"""
FILE: main.py
PURPOSE: Manages the core hardware monitoring logic and the vertically-centered dashboard interface.

KEY COMPONENTS:
1. DashboardTab CLASS: Uses a dual-stretch layout to pin the branding to the top and center metric cards.
2. AGGREGATED STORAGE LOGIC: Calculates a global system-wide storage percentage by summing total capacity vs total usage.
3. HARDWARE POLLING: Fetches real-time statistics for CPU, RAM, Disk, and GPU using 1000ms refresh cycles.
4. FLAMINPROAPP CLASS: The main window controller that manages the tabbed navigation and global stylesheets.
"""

"""
LIBRARIES USED:
1. psutil: Retrieves cross-platform system utilization data, now used for aggregate disk space summation.
2. GPUtil: Detects and monitors NVIDIA GPU load and status.
3. PySide6 (QtWidgets/QtCore): Powers the GUI architecture, layout management, and the refresh timer.
4. design (Local): Custom styling module for centralized branding and color management.
"""

import sys
import psutil
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, 
                             QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel)
from PySide6.QtCore import QTimer, Qt
import design 

try:
    import GPUtil
    HAS_GPU = True
except ImportError:
    HAS_GPU = False

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter) 
        main_layout.setContentsMargins(0, 40, 0, 30) 
        main_layout.setSpacing(0)

        # --- BRANDING HEADER GROUP ---
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(5) 
        header_layout.setContentsMargins(0, 0, 0, 20)

        self.brand_label = QLabel(design.APP_NAME)
        self.brand_label.setAlignment(Qt.AlignCenter)
        self.brand_label.setStyleSheet(f"font-size: 72px; font-weight: bold; color: {design.COLORS['primary']};")
        
        self.subtitle_label = QLabel(design.APP_SUBTITLE)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet(f"font-size: 16px; letter-spacing: 12px; color: #BBBBBB; padding-left: 12px; text-transform: uppercase;")
        
        header_layout.addWidget(self.brand_label)
        header_layout.addWidget(self.subtitle_label)
        main_layout.addWidget(header_widget)
        
        main_layout.addStretch(1) 

        # --- GRID OF CARDS ---
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setSpacing(25)

        self.cpu_card = self.create_card("🖥️ CPU USAGE", "0.0%")
        self.ram_card = self.create_card("🧠 RAM STATUS", "0.0%")
        self.disk_card = self.create_card("💾 STORAGE (TOTAL)", "0.0%")
        self.gpu_card = self.create_card("🎮 GPU LOAD", "N/A")

        grid.addWidget(self.cpu_card, 0, 0)
        grid.addWidget(self.ram_card, 0, 1)
        grid.addWidget(self.disk_card, 1, 0)
        grid.addWidget(self.gpu_card, 1, 1)

        main_layout.addWidget(grid_container, alignment=Qt.AlignCenter)
        main_layout.addStretch(1) 

        self.setLayout(main_layout)

    def create_card(self, title, start_val):
        card = QFrame()
        card.setFixedSize(400, 220)
        card.setStyleSheet(f"QFrame {{ background-color: {design.COLORS['surface']}; border: 2px solid {design.COLORS['primary']}; border-radius: 20px; padding: 20px; }}")
        v_layout = QVBoxLayout()
        t_label = QLabel(title)
        t_label.setStyleSheet("color: #888888; font-size: 12px; border: none; font-weight: bold;")
        val_label = QLabel(start_val)
        val_label.setStyleSheet(f"color: {design.COLORS['text']}; font-size: 48px; font-weight: 600; border: none;")
        card.value_label = val_label
        v_layout.addWidget(t_label)
        v_layout.addStretch() 
        v_layout.addWidget(val_label, alignment=Qt.AlignCenter)
        card.setLayout(v_layout)
        return card

    def update_dashboard(self):
        # 1. Update CPU and RAM
        self.cpu_card.value_label.setText(f"{psutil.cpu_percent()}%")
        self.ram_card.value_label.setText(f"{psutil.virtual_memory().percent}%")
        
        # 2. Aggregated Storage Logic
        try:
            total_used = 0
            total_capacity = 0
            # Get all fixed drives (skipping removable and network drives)
            for part in psutil.disk_partitions():
                if 'fixed' in part.opts or part.fstype:
                    try:
                        usage = psutil.disk_usage(part.mountpoint)
                        total_used += usage.used
                        total_capacity += usage.total
                    except PermissionError:
                        continue
            
            # Calculate total percentage across all drives
            if total_capacity > 0:
                aggregate_percent = (total_used / total_capacity) * 100
                self.disk_card.value_label.setText(f"{aggregate_percent:.1f}%")
            else:
                self.disk_card.value_label.setText("0.0%")
        except Exception:
            self.disk_card.value_label.setText("ERR")

        # 3. GPU logic
        if HAS_GPU:
            try:
                gpus = GPUtil.getGPUs()
                self.gpu_card.value_label.setText(f"{gpus[0].load*100:.1f}%" if gpus else "N/A")
            except: self.gpu_card.value_label.setText("ERR")
        else:
            self.gpu_card.value_label.setText("N/A")

class FlaminProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{design.APP_NAME} | {design.APP_SUBTITLE}")
        self.resize(1200, 900)
        self.setStyleSheet(design.get_main_style())
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.dashboard = DashboardTab()
        self.tabs.addTab(self.dashboard, "📊 DASHBOARD")
        self.tabs.addTab(QWidget(), "🎮 GPU")
        self.tabs.addTab(QWidget(), "💾 STORAGE")
        self.timer = QTimer()
        self.timer.timeout.connect(self.dashboard.update_dashboard)
        self.timer.start(1000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlaminProApp()
    window.show()
    sys.exit(app.exec())