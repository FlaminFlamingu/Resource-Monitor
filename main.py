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
        main_layout.setContentsMargins(0, 40, 0, 0)
        main_layout.setSpacing(30) # Space between header and cards

        # --- BRANDING HEADER GROUP ---
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(0) # Closes the vertical gap between names
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.brand_label = QLabel(design.APP_NAME)
        self.brand_label.setAlignment(Qt.AlignCenter)
        self.brand_label.setStyleSheet(f"""
            font-size: 72px; 
            font-weight: bold; 
            color: {design.COLORS['primary']};
            font-family: 'Segoe UI', sans-serif;
            margin-bottom: 0px;
        """)
        
        self.subtitle_label = QLabel(design.APP_SUBTITLE)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        # padding-left: 20px aligns it visually with the 'center' of the text above
        self.subtitle_label.setStyleSheet(f"""
            font-size: 16px; 
            letter-spacing: 12px; 
            color: #888888; 
            font-family: 'Segoe UI', sans-serif;
            font-weight: 300;
            text-transform: uppercase;
            padding-left: 20px; 
            margin-top: -5px;
        """)
        
        header_layout.addWidget(self.brand_label)
        header_layout.addWidget(self.subtitle_label)
        main_layout.addWidget(header_widget)

        # --- GRID OF CARDS ---
        grid = QGridLayout()
        grid.setSpacing(25)

        self.cpu_card = self.create_card("🖥️ CPU USAGE", "0.0%")
        self.ram_card = self.create_card("🧠 RAM STATUS", "0.0%")
        self.disk_card = self.create_card("💾 STORAGE (AVG)", "0.0%")
        self.gpu_card = self.create_card("🎮 GPU LOAD", "N/A")

        grid.addWidget(self.cpu_card, 0, 0)
        grid.addWidget(self.ram_card, 0, 1)
        grid.addWidget(self.disk_card, 1, 0)
        grid.addWidget(self.gpu_card, 1, 1)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def create_card(self, title, start_val):
        card = QFrame()
        card.setFixedSize(400, 200) 
        card.setStyleSheet(f"""
            QFrame {{ 
                background-color: {design.COLORS['surface']}; 
                border: 2px solid {design.COLORS['primary']}; 
                border-radius: 20px; 
                padding: 20px; 
            }}
        """)
        v_layout = QVBoxLayout()
        t_label = QLabel(title)
        t_label.setStyleSheet("color: #888888; font-size: 12px; border: none; font-weight: bold;")
        
        val_label = QLabel(start_val)
        val_label.setStyleSheet(f"""
            color: {design.COLORS['text']}; 
            font-size: 48px; 
            font-weight: 600; 
            font-family: 'Segoe UI';
            border: none;
        """)
        
        card.value_label = val_label
        v_layout.addWidget(t_label)
        v_layout.addStretch() 
        v_layout.addWidget(val_label, alignment=Qt.AlignCenter)
        card.setLayout(v_layout)
        return card

    def update_dashboard(self):
        self.cpu_card.value_label.setText(f"{psutil.cpu_percent()}%")
        self.ram_card.value_label.setText(f"{psutil.virtual_memory().percent}%")
        try:
            disks = [psutil.disk_usage(p.mountpoint).percent for p in psutil.disk_partitions() if 'fixed' in p.opts]
            avg = sum(disks) / len(disks) if disks else 0
            self.disk_card.value_label.setText(f"{avg:.1f}%")
        except: self.disk_card.value_label.setText("ERR")

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
        self.resize(1100, 850)
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