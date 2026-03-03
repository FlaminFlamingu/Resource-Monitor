"""
FILE: design.py
PURPOSE: Defines the visual identity, branding elements, and global UI styles for the FlaminFlamingu Resource Monitor.

KEY COMPONENTS:
1. BRANDING CONSTANTS: Stores the official 'FlaminFlamingu' name and subtitle strings.
2. THEME ENGINE: Contains the 'COLORS' dictionary with a high-contrast Pink & Black palette.
3. ASCII ART: Provides a raw string logo optimized for terminal output and header styling.
4. CSS ENGINE: Generates a dynamic QSS (Qt Style Sheet) to skin the main window, tabs, and labels.
"""

"""
LIBRARIES USED:
1. PySide6: Implicitly targets this framework for style sheet parsing and widget skinning.
2. Segoe UI: The primary system font for a modern, clean UI appearance.
3. Raw Strings (r""): Prevents Python from misinterpreting backslashes in the ASCII art logo.
"""

# Branding strings for the application header and window title
APP_NAME = "FlaminFlamingu"
APP_SUBTITLE = "RESOURCE MONITOR"

# High-contrast Pink & Black theme colors
COLORS = {
    "primary": "#FF1493",    # Hot Pink (Deep Pink)
    "background": "#000000", # Pure Black
    "surface": "#1A1A1A",    # Dark Grey for panels
    "text": "#FFFFFF",       # White
    "accent": "#FF69B4"      # Lighter Pink (HotPink)
}

# Raw string ASCII art for the branding logo
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
    # Compiles the global QSS (Qt Style Sheet) for the application
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