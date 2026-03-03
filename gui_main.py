"""
FILE: main.py
PURPOSE: Acts as the entry point and core logic engine for the FlaminFlamingu Resource Monitor.

KEY COMPONENTS:
1. FlaminProApp CLASS: The main window controller that initializes the UI, tabs, and global styles.
2. THEME INTEGRATION: Dynamically imports branding and CSS from design.py to maintain a decoupled architecture.
3. EXECUTION LAYER: Handles the application lifecycle, including the event loop and terminal-side ASCII branding.
"""

"""
LIBRARIES USED:
1. sys: Provides access to system-specific parameters and functions, primarily used for clean application exit.
2. PySide6.QtWidgets: The primary toolkit for creating the GUI components (QMainWindow, QTabWidget, etc.).
3. design (Custom): Local module containing centralized styles, colors, and branding constants.
"""

import sys
import design 
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

class FlaminProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Sets the window title using the string defined in design.py
        self.setWindowTitle(design.APP_NAME)
        
        # Defines the default startup size of the application window
        self.resize(900, 600)
        
        # Injects the centralized CSS stylesheet into the application
        self.setStyleSheet(design.get_main_style())
        
        # ... logic for tabs and hardware monitoring will go here ...

if __name__ == "__main__":
    # Initializes the Qt application instance
    app = QApplication(sys.argv)
    
    # Outputs the branding logo to the console for developer feedback
    print(design.BRAND_ASCII) 
    
    # Creates and displays the main application window
    window = FlaminProApp()
    window.show()
    
    # Starts the event loop and ensures a clean system exit
    sys.exit(app.exec())