import sys
import design  # Import your updated design file
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

class FlaminProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Pull the name directly from design.py
        self.setWindowTitle(design.APP_NAME)
        self.resize(900, 600)
        
        # Apply the Pro Styles
        self.setStyleSheet(design.get_main_style())
        
        # ... the rest of your tab logic ...

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Print the ASCII to the terminal when starting (Cool dev touch)
    print(design.BRAND_ASCII) 
    
    window = FlaminProApp()
    window.show()
    sys.exit(app.exec())