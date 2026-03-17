"""
FILE DESCRIPTION KEY COMPONENTS:
1. THEME: Global color palette (Pink/Black/Gray).
2. METRIC CARD: The base widget for the dashboard boxes.
"""

"""
LIBRARIES USED:
1. PySide6: QFrame and QLabel for styling.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

APP_NAME = "FlaminFlamingu"
APP_SUBTITLE = "RESOURCE MONITOR"

COLORS = {
    "primary": "#FF1493",
    "background": "#000000",
    "surface": "#1A1A1A",
    "text": "#FFFFFF",
    "muted": "#888888"
}

def get_main_style():
    # Global QSS for tabs and background
    return f"""
        QMainWindow {{ background-color: {COLORS['background']}; }}
        QTabWidget::pane {{ border: 1px solid {COLORS['surface']}; background-color: {COLORS['background']}; }}
        QTabBar::tab {{
            background: {COLORS['surface']}; color: {COLORS['text']}; padding: 12px 25px;
            border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 4px;
            border: 1px solid #333; font-family: 'Segoe UI'; font-size: 13px;
        }}
        QTabBar::tab:selected {{ background: {COLORS['primary']}; color: white; font-weight: bold; }}
    """

class MetricCard(QFrame):
    # The large box style from your reference image
    def __init__(self, title, start_val):
        super().__init__()
        self.setFixedSize(420, 240) 
        self.setStyleSheet(f"background-color: {COLORS['surface']}; border: 2px solid {COLORS['primary']}; border-radius: 25px; padding: 20px;")
        
        layout = QVBoxLayout(self)
        self.t_label = QLabel(title)
        self.t_label.setStyleSheet(f"color: {COLORS['muted']}; font-size: 11px; font-weight: bold; border: none;")
        
        self.v_label = QLabel(start_val)
        self.v_label.setStyleSheet("color: white; font-size: 64px; font-weight: bold; border: none;")
        
        layout.addWidget(self.t_label)
        layout.addStretch()
        layout.addWidget(self.v_label, alignment=Qt.AlignCenter)
        layout.addStretch()