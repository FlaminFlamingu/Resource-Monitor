"""
FILE: design.py
PURPOSE: Combined styling engine and Dashboard UI components for FlaminFlamingu.

FILE DESCRIPTION KEY COMPONENTS:
1. THEME ENGINE: Centralized 'COLORS' and global QSS generator.
2. DASHBOARD UI: MetricCard and DashboardTab classes with refined centering and gray sub-text.
3. BRANDING: Centered titles with specific color layering (Pink vs Gray).
"""

"""
LIBRARIES USED:
1. PySide6: GUI components (QWidget, QFrame, QLabel, etc.).
2. psutil: System metric retrieval for CPU, RAM, and Storage Calculation.
3. GPUtil: NVIDIA GPU monitoring (optional).
"""

import os
import psutil
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel
from PySide6.QtCore import Qt

# Check for GPU monitoring support
try:
    import GPUtil
    HAS_GPU = True
except ImportError:
    HAS_GPU = False

# Branding strings
APP_NAME = "FlaminFlamingu"
APP_SUBTITLE = "RESOURCE MONITOR"

# High-contrast Pink & Black theme colors
COLORS = {
    "primary": "#FF1493",    # Hot Pink
    "background": "#000000", # Pure Black
    "surface": "#1A1A1A",    # Dark Grey for cards
    "text": "#FFFFFF",       # White
    "muted": "#888888"       # Gray for sub-labels and subtitles
}

def get_main_style():
    # Compiles the global QSS for the application
    return f"""
        QMainWindow {{ background-color: {COLORS['background']}; }}
        QTabWidget::pane {{ border: 1px solid {COLORS['surface']}; background-color: {COLORS['background']}; }}
        QTabBar::tab {{
            background: {COLORS['surface']}; color: {COLORS['text']}; padding: 12px 25px;
            border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 4px;
            border: 1px solid #333; font-family: 'Segoe UI'; font-size: 13px;
        }}
        QTabBar::tab:selected {{ background: {COLORS['primary']}; color: white; font-weight: bold; }}
        QLabel {{ color: {COLORS['text']}; font-family: 'Segoe UI', sans-serif; }}
    """

# --- Dashboard UI Classes ---

class MetricCard(QFrame):
    # Large centered boxes for information display
    def __init__(self, title, start_val):
        super().__init__()
        # Increased box size to match visual reference
        self.setFixedSize(420, 240) 
        self.setStyleSheet(f"""
            QFrame {{ 
                background-color: {COLORS['surface']}; 
                border: 2px solid {COLORS['primary']}; 
                border-radius: 25px; 
                padding: 20px; 
            }}
        """)
        layout = QVBoxLayout(self)
        
        # Category label in gray
        self.t_label = QLabel(title)
        self.t_label.setStyleSheet(f"color: {COLORS['muted']}; font-size: 11px; font-weight: bold; border: none;")
        
        # Main metric value in white
        self.value_label = QLabel(start_val)
        self.value_label.setStyleSheet("color: white; font-size: 64px; font-weight: bold; border: none;")
        
        layout.addWidget(self.t_label)
        layout.addStretch() 
        layout.addWidget(self.value_label, alignment=Qt.AlignCenter)
        layout.addStretch()

class DashboardTab(QWidget):
    # Centered landing page with gray sub-text
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        # Force everything to the center of the screen
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        # Title Stack
        title_stack = QWidget()
        ts_layout = QVBoxLayout(title_stack)
        ts_layout.setSpacing(5)
        
        # Pink branding
        header = QLabel(APP_NAME)
        header.setStyleSheet(f"font-size: 72px; font-weight: bold; color: {COLORS['primary']}; border: none;")
        header.setAlignment(Qt.AlignCenter)
        
        # Gray wide subtitle
        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setStyleSheet(f"""
            font-size: 18px; 
            color: {COLORS['muted']}; 
            letter-spacing: 12px; 
            font-weight: 400; 
            border: none;
            margin-left: 12px; 
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        ts_layout.addWidget(header)
        ts_layout.addWidget(subtitle)
        
        # Grid for the info boxes
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setSpacing(25) 
        
        self.cpu_card = MetricCard("🖥️ CPU USAGE", "0.0%")
        self.ram_card = MetricCard("🧠 RAM STATUS", "0.0%")
        self.disk_card = MetricCard("💾 TOTAL STORAGE", "0.0%")
        self.gpu_card = MetricCard("🎮 GPU LOAD", "N/A")
        
        grid.addWidget(self.cpu_card, 0, 0)
        grid.addWidget(self.ram_card, 0, 1)
        grid.addWidget(self.disk_card, 1, 0)
        grid.addWidget(self.gpu_card, 1, 1)
        
        main_layout.addWidget(title_stack)
        main_layout.addSpacing(40) 
        main_layout.addWidget(grid_container)

    def update_metrics(self):
        # Refresh logic called by the main timer
        self.cpu_card.value_label.setText(f"{psutil.cpu_percent():.1f}%")
        self.ram_card.value_label.setText(f"{psutil.virtual_memory().percent:.1f}%")
        
        # Aggregate storage percentage across all drives
        try:
            total_used = 0
            total_cap = 0
            for part in psutil.disk_partitions():
                if 'fixed' in part.opts or part.fstype:
                    try:
                        usage = psutil.disk_usage(part.mountpoint)
                        total_used += usage.used
                        total_cap += usage.total
                    except PermissionError:
                        continue
            
            if total_cap > 0:
                total_percent = (total_used / total_cap) * 100
                total_gb = total_cap / (1024**3)
                self.disk_card.value_label.setText(f"{total_percent:.1f}%")
                self.disk_card.t_label.setText(f"💾 TOTAL STORAGE ({total_gb:.0f} GB TOTAL)")
            else:
                self.disk_card.value_label.setText("N/A")
        except:
            self.disk_card.value_label.setText("N/A")
            
        if HAS_GPU:
            gpus = GPUtil.getGPUs()
            self.gpu_card.value_label.setText(f"{gpus[0].load*100:.1f}%" if gpus else "N/A")