"""
FILE: gpu_monitor.py
PURPOSE: Monitors dedicated NVIDIA graphics hardware performance and vitals.

KEY COMPONENTS:
1. THERMAL TRACKING: Reports real-time core temperature in Celsius.
2. LOAD MONITOR: Tracks GPU processing utilization percentage.
3. VRAM ANALYZER: Reports video memory allocation and total capacity.
"""

"""
LIBRARIES USED:
1. GPUtil: Interface for NVIDIA Management Library (NVML).
2. PySide6: UI labels and layout management.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
import design

# Global check to see if the required library is installed
try:
    import GPUtil
    HAS_GPU_LIB = True
except ImportError:
    HAS_GPU_LIB = False

class GPUTab(QWidget):
    def __init__(self):
        super().__init__()
        # Main layout for the GPU slide
        self.layout = QVBoxLayout(self)
        
        # Header for the GPU analysis page
        title = QLabel("GPU HARDWARE ANALYSIS")
        title.setStyleSheet(f"color: {design.COLORS['primary']}; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(title)

        # Create a container card for the GPU stats
        self.card = QFrame()
        self.card.setStyleSheet(f"background: {design.COLORS['surface']}; border-radius: 15px; padding: 20px;")
        self.card_layout = QVBoxLayout(self.card)
        
        # Labels for different metrics
        self.model_label = QLabel("Detecting GPU...")
        self.model_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        
        self.load_label = QLabel("Load: --%")
        self.temp_label = QLabel("Temp: --°C")
        self.mem_label = QLabel("VRAM: -- / -- MB")
        
        # Style the metric labels
        for lbl in [self.load_label, self.temp_label, self.mem_label]:
            lbl.setStyleSheet(f"color: {design.COLORS['text']}; font-size: 16px; margin-top: 5px;")

        self.card_layout.addWidget(self.model_label)
        self.card_layout.addWidget(self.load_label)
        self.card_layout.addWidget(self.temp_label)
        self.card_layout.addWidget(self.mem_label)
        
        self.layout.addWidget(self.card)
        self.layout.addStretch()

    def update_gpu(self):
        # Polled by main.py every 1000ms
        if not HAS_GPU_LIB:
            self.model_label.setText("GPUtil Library Missing")
            return

        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0] # Monitors the primary card
                self.model_label.setText(f"🎮 {gpu.name}")
                self.load_label.setText(f"Load: {gpu.load * 100:.1f}%")
                self.temp_label.setText(f"Temperature: {gpu.temperature}°C")
                self.mem_label.setText(f"VRAM: {int(gpu.memoryUsed)}MB / {int(gpu.memoryTotal)}MB")
            else:
                self.model_label.setText("No NVIDIA GPU Detected")
        except Exception:
            self.model_label.setText("GPU Data Unavailable")