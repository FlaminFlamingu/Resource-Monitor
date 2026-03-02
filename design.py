# design.py - Centralized Branding & Styles

APP_NAME = "FlaminFlamingu"
APP_SUBTITLE = "RESOURCE MONITOR"

# PINK & BLACK THEME
COLORS = {
    "primary": "#FF1493",    # Hot Pink (Deep Pink)
    "background": "#000000", # Pure Black
    "surface": "#1A1A1A",    # Dark Grey for panels
    "text": "#FFFFFF",       # White
    "accent": "#FF69B4"      # Lighter Pink (HotPink)
}

# Corrected Full ASCII: "FlaminFlamingu"
BRAND_ASCII = r"""
  ______ _                 _       ______ _                 _                       
 |  ____| |               (_)     |  ____| |               (_)                      
 | |__  | | __ _ _ __ ___  _ _ __ | |__  | | __ _ _ __ ___  _ _ __   __ _ _   _ 
 |  __| | |/ _` | '_ ` _ \| | '_ \|  __| | |/ _` | '_ ` _ \| | '_ \ / _` | | | |
 | |    | | (_| | | | | | | | | | | |    | | (_| | | | | | | | | | | (_| | |_| |
 |_|    |_|\__,_|_| |_| |_|_|_| |_|_|    |_|\__,_|_| |_| |_|_|_| |_|\__, |\__,_|
                                                                     __/ |      
                         RESOURCE MONITOR                           |___/       
"""

def get_main_style():
    """Returns the CSS-style sheet for the PySide6 UI."""
    return f"""
        QMainWindow {{ 
            background-color: {COLORS['background']}; 
        }}
        QTabWidget::pane {{ 
            border: 1px solid {COLORS['surface']}; 
            background-color: {COLORS['background']};
        }}
        QTabBar::tab {{
            background: {COLORS['surface']};
            color: {COLORS['text']};
            padding: 12px 20px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin-right: 2px;
            border: 1px solid #333;
        }}
        QTabBar::tab:selected {{
            background: {COLORS['primary']};
            color: white;
            font-weight: bold;
        }}
        QLabel {{ 
            color: {COLORS['text']}; 
            font-family: 'Segoe UI', sans-serif; 
        }}
    """