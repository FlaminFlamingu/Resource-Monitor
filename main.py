import sys
import psutil
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, 
                             QWidget, QVBoxLayout, QLabel)
from PySide6.QtCore import QTimer, Qt
import pyqtgraph as pg

# This pulls your ASCII, APP_NAME, and COLORS
import design 

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # --- NEW BRANDING HEADER ---
        self.brand_label = QLabel(design.APP_NAME)
        self.brand_label.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {design.COLORS['primary']}; margin-bottom: 0px;")
        
        self.subtitle_label = QLabel(design.APP_SUBTITLE)
        self.subtitle_label.setStyleSheet("font-size: 14px; letter-spacing: 2px; color: #888888; margin-top: -5px; margin-bottom: 20px;")
        # ---------------------------

        self.graph_label = QLabel("LIVE CPU PERFORMANCE")
        self.graph_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #FFFFFF;")
        
        # Pro Graph Setup
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('#121212')
        self.graph_widget.setYRange(0, 100)
        self.graph_widget.showGrid(x=True, y=True, alpha=0.3) 
        
        # Style the line with your primary color from design.py
        self.data_line = self.graph_widget.plot([], [], pen=pg.mkPen(color=design.COLORS['primary'], width=3))
        
        self.x = list(range(50))
        self.y = [0] * 50
        
        # Add everything to the layout
        layout.addWidget(self.brand_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.graph_label)
        layout.addWidget(self.graph_widget)
        self.setLayout(layout)

    def update_plot(self):
        """Standard method to update the graph data"""
        self.y = self.y[1:]
        self.y.append(psutil.cpu_percent())
        self.data_line.setData(self.x, self.y)

class FlaminProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Use branding from design.py for the window title
        self.setWindowTitle(f"{design.APP_NAME} | {design.APP_SUBTITLE}")
        self.resize(1000, 600)
        self.setStyleSheet(design.get_main_style())

        # Create the Tab System
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize the Dashboard
        self.dashboard = DashboardTab()
        self.tabs.addTab(self.dashboard, "📊 DASHBOARD")
        
        # Placeholders for future tabs
        self.tabs.addTab(QWidget(), "🎮 GPU LAB")
        self.tabs.addTab(QWidget(), "💾 STORAGE")

        # Live Update Timer (Runs every 1000ms / 1 second)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.dashboard.update_plot)
        self.timer.start()

if __name__ == "__main__":
    # Print the branding to terminal for logs
    print(design.BRAND_ASCII)
    
    app = QApplication(sys.argv)
    window = FlaminProApp()
    window.show()
    sys.exit(app.exec())