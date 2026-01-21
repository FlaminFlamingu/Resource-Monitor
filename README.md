# FlaminFlamingu Resource-Monitor

A lightweight, terminal-based system monitoring tool designed for clarity and speed. Inspired by the efficiency of Task Manager, this project strips away the clutter to give you exactly the resource data you need in an easy-to-navigate ASCII dashboard.

## 🚀 Purpose
The goal of this project is to provide a "clean-view" resource output. Unlike heavy GUI applications, **FlaminFlamingu Resource-Monitor** focuses on providing high-readability data for CPU, GPU, Memory, and Storage with zero distractions. It is built to be a modular framework that others can use as inspiration for their own monitoring tools.

## ✨ Key Features
* **Focused Data:** Only shows essential metrics (Load, Temp, VRAM, RAM, and Disk) for quick navigation.
* **Universal GPU Support:** Integrated logic for both NVIDIA (GPUtil) and AMD (pyadl) hardware.
* **Modular Architecture:** Hardware logic is separated from the UI, making it easy to study or expand.
* **Visual Clarity:** Uses a custom-built ANSI color-coded ASCII dashboard for a professional terminal look.

## 🛠️ Installation
Currently, this project runs as a Python script. You will need to install the following dependencies:

```bash
pip install psutil GPUtil pyadl wmi py-cpuinfo
Note: A setup script is currently in development to automate this process for a one-click installation experience.

I have formatted the entire README.md into a single, clean Markdown block so you can copy and paste the whole thing at once.

Markdown

# FlaminFlamingu Resource-Monitor

A lightweight, terminal-based system monitoring tool designed for clarity and speed. Inspired by the efficiency of Task Manager, this project strips away the clutter to give you exactly the resource data you need in an easy-to-navigate ASCII dashboard.

## 🚀 Purpose
The goal of this project is to provide a "clean-view" resource output. Unlike heavy GUI applications, **FlaminFlamingu Resource-Monitor** focuses on providing high-readability data for CPU, GPU, Memory, and Storage with zero distractions. It is built to be a modular framework that others can use as inspiration for their own monitoring tools.

## ✨ Key Features
* **Focused Data:** Only shows essential metrics (Load, Temp, VRAM, RAM, and Disk) for quick navigation.
* **Universal GPU Support:** Integrated logic for both NVIDIA (GPUtil) and AMD (pyadl) hardware.
* **Modular Architecture:** Hardware logic is separated from the UI, making it easy to study or expand.
* **Visual Clarity:** Uses a custom-built ANSI color-coded ASCII dashboard for a professional terminal look.

## 🛠️ Installation
Currently, this project runs as a Python script. You will need to install the following dependencies:

```bash
pip install psutil GPUtil pyadl wmi py-cpuinfo
Note: A setup script is currently in development to automate this process for a one-click installation experience.

📂 Project Structure
main.py: The engine that runs the timing loop and coordinates data between monitors and the UI.

design.py: The UI layer containing the dashboard layout, ASCII borders, and the full ANSI color palette.

Monitors/: A dedicated package containing individual logic scripts for:

cpu_monitor.py

gpu_monitor.py

memory_monitor.py

disk_monitor.py

🚦 How to Use
Step 1: Open the Command Interface
Open your terminal of choice. On Windows, press the Win key, type cmd, and press Enter. For a more modern experience, you may also use PowerShell or Windows Terminal.

Step 2: Navigate to the Repository
You must point the command prompt to the folder where you have saved the script. Copy the folder path from your file explorer and use the cd (Change Directory) command:
cd C:\Users\YourName\Documents\RESOURCE-MONITOR

Step 3: Initialize the Script
Once your terminal is mapped to the correct directory, execute the main entry point of the application using the Python interpreter:
py main.py
Note: Depending on your system configuration, you may need to use python main.py or python3 main.py.

Step 4: Monitoring
The dashboard will now initialize. The interface will refresh in real-time. To safely terminate the process and return to the command line, use the keyboard shortcut Ctrl + C.

🗺️ Roadmap
I am actively building toward several major milestones:

[ ] Automated Setup: A Python or Batch script to handle all library installations.

[ ] Application Conversion: Compiling the script into a standalone executable (.exe) for non-Python users.

[ ] Individual Process Tracking: The ability to check resource usage of specific apps before or while they run.

[ ] Web Interface: A browser-based version of the dashboard for remote monitoring across a network.

⚖️ License & Contribution
This project is shared publicly for inspiration and educational purposes. You are encouraged to study the code and use the logic to build your own unique monitors.

Contribution Policy: At this stage, I am not accepting direct pull requests or changes to the core codebase as I am finishing the primary build. However, feel free to fork the project to experiment with your own versions!