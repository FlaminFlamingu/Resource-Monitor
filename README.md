# 🔥 FlaminFlamingu Resource-Monitor

![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.14-blue?logo=python)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/license-Educational-orange)
![Status](https://img.shields.io/badge/status-v1.0.0--Stable-success)

A lightweight, high-performance terminal dashboard designed for clarity. Inspired by the Windows Task Manager, **FlaminFlamingu** strips away the bloat to deliver pure hardware metrics in a professional ASCII interface.

---

## 🚀 Purpose
Modern GUI monitors are heavy and resource-intensive. This project provides a **clean-view** resource output with zero distractions. It is built as a modular framework, allowing developers to study the logic or expand it for their own custom hardware monitoring tools.

## ✨ Key Features
* **🎯 Focused Metrics:** Real-time monitoring of CPU, GPU, RAM, and Storage.
* **💻 Hybrid GPU Support:** Intelligent detection for laptops (Seamless iGPU vs. dGPU tracking).
* **🔌 Live USB Detector:** Dedicated **Orange Alert Box** for real-time hardware hot-plugging.
* **🎨 Visual Clarity:** ANSI color-coded dashboard for a professional, "hacker-style" terminal look.
* **📦 Standalone:** Compiled `.exe` support—no Python installation required for end-users.

## 📂 Project Structure
```t
RESOURCE-MONITOR/
├── assets/             # Branding assets (icon.ico)
├── Monitors/           # Specialized logic for each component
│   ├── cpu_monitor.py  # Thermal & Load tracking
│   ├── gpu_monitor.py  # Hybrid NVIDIA/AMD logic
│   ├── usb_monitor.py  # Hardware event polling
│   ├── memory_monitor.py
│   └── disk_monitor.py
├── design.py           # UI Layer & ASCII Layout
└── main.py             # Execution Engine

🛠️ **Installation & Usage**
[!IMPORTANT]
Administrative Privileges Required: To access deep hardware sensors (like CPU Temperature), you MUST run your terminal or the .exe as an Administrator. Without elevation, some data will show as "N/A".

Option A: The Executable (Fastest)
Navigate to the dist/ folder in this repository.

Right-click FlaminFlaminguMonitor.exe.

Select Run as Administrator.

Option B: Running from Source
Clone the repository:

Bash

git clone [https://github.com/YourUsername/FlaminFlamingu-Monitor.git](https://github.com/YourUsername/FlaminFlamingu-Monitor.git)
Install Dependencies:

Bash

pip install psutil GPUtil pyadl wmi py-cpuinfo setuptools
Launch the application:

Bash

python main.py

Gemini said
I understand—you want the raw code block so you can copy the entire file contents without any of my extra commentary or formatting getting in the way.

Markdown
# 🔥 FlaminFlamingu Resource-Monitor

![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.14-blue?logo=python)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/license-Educational-orange)
![Status](https://img.shields.io/badge/status-v1.0.0--Stable-success)

A lightweight, high-performance terminal dashboard designed for clarity. Inspired by the Windows Task Manager, **FlaminFlamingu** strips away the bloat to deliver pure hardware metrics in a professional ASCII interface.

---

## 🚀 Purpose
Modern GUI monitors are heavy and resource-intensive. This project provides a **clean-view** resource output with zero distractions. It is built as a modular framework, allowing developers to study the logic or expand it for their own custom hardware monitoring tools.

## ✨ Key Features
* **🎯 Focused Metrics:** Real-time monitoring of CPU, GPU, RAM, and Storage.
* **💻 Hybrid GPU Support:** Intelligent detection for laptops (Seamless iGPU vs. dGPU tracking).
* **🔌 Live USB Detector:** Dedicated **Orange Alert Box** for real-time hardware hot-plugging.
* **🎨 Visual Clarity:** ANSI color-coded dashboard for a professional, "hacker-style" terminal look.
* **📦 Standalone:** Compiled `.exe` support—no Python installation required for end-users.

## 📂 Project Structure
```text
RESOURCE-MONITOR/
├── assets/             # Branding assets (icon.ico)
├── Monitors/           # Specialized logic for each component
│   ├── cpu_monitor.py  # Thermal & Load tracking
│   ├── gpu_monitor.py  # Hybrid NVIDIA/AMD logic
│   ├── usb_monitor.py  # Hardware event polling
│   ├── memory_monitor.py
│   └── disk_monitor.py
├── design.py           # UI Layer & ASCII Layout
└── main.py             # Execution Engine
🛠️ Installation & Usage
[!IMPORTANT]
Administrative Privileges Required: To access deep hardware sensors (like CPU Temperature), you MUST run your terminal or the .exe as an Administrator. Without elevation, some data will show as "N/A".

Option A: The Executable (Fastest)
Navigate to the dist/ folder in this repository.

Right-click FlaminFlaminguMonitor.exe.

Select Run as Administrator.

Option B: Running from Source
Clone the repository:

Bash
git clone [https://github.com/YourUsername/FlaminFlamingu-Monitor.git](https://github.com/YourUsername/FlaminFlamingu-Monitor.git)
Install Dependencies:

Bash
pip install psutil GPUtil pyadl wmi py-cpuinfo setuptools
Launch the application:

Bash
python main.py
🗺️ Roadmap
[x] USB Detector: Real-time hardware event polling.

[x] Hybrid GPU Support: iGPU and dGPU detection for mobile workstations.

[x] Application Conversion: Compiled standalone .exe with custom branding.

[ ] Individual Process Tracking: View resource usage of specific active apps.

[ ] Web Interface: Browser-based dashboard for remote network monitoring.

⚖️ License & Contribution
This project is shared publicly for inspiration and educational purposes. You are encouraged to study the code and use the logic to build your own unique monitors.

Contribution Policy: At this stage, I am not accepting direct pull requests as I am finalizing the primary build features. However, feel free to fork the project to experiment with your own versions!