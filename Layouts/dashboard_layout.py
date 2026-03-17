"""
FILE DESCRIPTION KEY COMPONENTS:
1. BRANDING HEADER: Centered Hot Pink title with the gray RESOURCE MONITOR subtitle.
2. GRID LAYOUT: Organizes MetricCards into a balanced 2x2 presentation.
"""

"""
LIBRARIES USED:
1. PySide6: Layout management.
2. design: Theme constants and styling.
"""

from PySide6.QtWidgets import QVBoxLayout, QGridLayout, QWidget, QLabel
from PySide6.QtCore import Qt
import design

def build_dashboard_layout(parent_tab, cards):
    # This script handles the structural positioning of the dashboard components
    main_layout = QVBoxLayout(parent_tab)
    main_layout.setAlignment(Qt.AlignCenter)
    main_layout.setContentsMargins(0, 0, 0, 0)

    # 1. Branding Header
    header_container = QWidget()
    h_layout = QVBoxLayout(header_container)
    
    title = QLabel(design.APP_NAME)
    title.setStyleSheet(f"font-size: 72px; font-weight: bold; color: {design.COLORS['primary']}; border: none;")
    title.setAlignment(Qt.AlignCenter)
    
    subtitle = QLabel(design.APP_SUBTITLE)
    subtitle.setStyleSheet(f"font-size: 18px; color: {design.COLORS['muted']}; letter-spacing: 12px; font-weight: 400; border: none; margin-left: 12px;")
    subtitle.setAlignment(Qt.AlignCenter)
    
    h_layout.addWidget(title)
    h_layout.addWidget(subtitle)
    
    # 2. Metric Grid
    grid_container = QWidget()
    grid = QGridLayout(grid_container)
    grid.setSpacing(25)
    
    grid.addWidget(cards['cpu'], 0, 0)
    grid.addWidget(cards['ram'], 0, 1)
    grid.addWidget(cards['disk'], 1, 0)
    grid.addWidget(cards['gpu'], 1, 1)
    
    main_layout.addWidget(header_container)
    main_layout.addSpacing(40)
    main_layout.addWidget(grid_container)