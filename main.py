"""
FILE DESCRIPTION KEY COMPONENTS:
1. APP ENGINE: Initializes FlaminFlamingu and the Tab system.
2. UPDATER: Orchestrates the data flow between Monitors and Layout components.
"""

"""
LIBRARIES USED:
1. PySide6: Main app loop and timing.
2. design, Monitors, Layouts: Modular project components.
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget
from PySide6.QtCore import QTimer

# Ensure modules in subfolders are imported correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import design
from Monitors import dashboard_monitor
from Layouts import dashboard_layout

class FlaminFlamingu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{design.APP_NAME} | {design.APP_SUBTITLE}")
        self.setStyleSheet(design.get_main_style())
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Dashboard Tab Initialization
        self.dash_tab = QWidget()
        self.cards = {
            'cpu': design.MetricCard("🖥️ CPU USAGE", "0.0%"),
            'ram': design.MetricCard("🧠 RAM STATUS", "0.0%"),
            'disk': design.MetricCard("💾 TOTAL STORAGE", "0.0%"),
            'gpu': design.MetricCard("🎮 GPU LOAD", "N/A")
        }
        
        # Assembly
        dashboard_layout.build_dashboard_layout(self.dash_tab, self.cards)
        self.tabs.addTab(self.dash_tab, "📊 DASHBOARD")

        # Start the update loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    def update_stats(self):
        # Retrieve metrics from the monitor script
        data = dashboard_monitor.get_dashboard_metrics()
        
        # Update the UI card labels
        self.cards['cpu'].v_label.setText(f"{data['cpu']:.1f}%")
        self.cards['ram'].v_label.setText(f"{data['ram']:.1f}%")
        self.cards['disk'].v_label.setText(f"{data['storage_pct']:.1f}%")
        self.cards['disk'].t_label.setText(f"💾 TOTAL STORAGE ({data['storage_total']:.0f} GB TOTAL)")
        
        gpu = data['gpu']
        self.cards['gpu'].v_label.setText(f"{gpu:.1f}%" if isinstance(gpu, float) else gpu)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlaminFlamingu()
    window.showMaximized()
    sys.exit(app.exec())