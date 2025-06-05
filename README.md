# Camel Time

A Windows application for monitoring and tracking process execution time with detailed usage statistics.

## Overview

Camel Time is a system monitoring tool that tracks the runtime of selected processes, providing comprehensive statistics about application usage. The application runs in the system tray and offers real-time monitoring capabilities with automatic data persistence.

## Features

- Real-time process monitoring
- System tray integration
- Automatic data saving with configurable intervals
- Customizable process tracking
- Windows autostart support
- New process detection and notification
- GUI interface for statistics and configuration

## System Requirements

- Windows 10/11
- Python 3.12.1 or higher
- Required packages: customtkinter, pillow, pystray, psutil

## Installation

### Option 1: Executable
1. Download .exe file
2. Run the executable
3. Configuration files will be created automatically

### Option 2: Source Code
1. Install Python 3.12.1
2. Install dependencies:
   ```bash
   pip install requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

- **Root Directory**
  - `main.py` - Application entry point
  - `globals.py` - Global variables and constants
  - `requirements.txt` - Python dependencies

- **assets/** - Static resources
  - `icon.png` - Application icon
  - `settings.png` - Settings icon

- **gui/** - User interface components
  - `__init__.py`
  - `stats_root.py` - Main statistics window
  - `input_dialog.py` - Input dialog component
  - `confirmation_dialog.py` - Confirmation dialog component

- **utils/** - Utility modules
  - `__init__.py`
  - `config_operations.py` - Configuration management
  - `file_operations.py` - File I/O operations
  - `process_monitor.py` - Process monitoring logic
  - `tray_icon.py` - System tray functionality



## Configuration Parameters

- `max_autosaves`: Maximum number of automatic backup files
- `autosave_delay_sec`: Interval between automatic saves (seconds)
- `new_process_window_time_sec`: Duration for new process notification display
- `runned_process_time_sec`: Retention time for process run history
- `open_window_on_start`: Show the main window on application startup
- `autostart`: Enable Windows autostart

## Usage

### Adding Processes for Tracking
1. When a new process starts, a notification dialog appears
2. Select "Yes" to add the process to tracking
3. Enter a display name for the process

### Viewing Statistics
- Right-click the system tray icon and select "Open statistic"
- Statistics window shows tracked processes with runtime information

### Managing Tracked Processes
- Add processes: Use the "Add tracked process" button in the main window
- Remove processes: Use the "Delete tracked program" button and select the process to remove
- Configure settings: Access through the settings button

## Data Management

### Data Storage
- Process data is stored in JSON format in `data.json`
- Tracked processes include runtime, PID, display name, and last run time
- Process run history is maintained with automatic cleanup

### Automatic Backup
- Periodic backups are created in the `Autosaves/` directory
- Backup frequency is controlled by `autosave_delay_sec`
- Amount-retained backups is limited by `max_autosaves`

## Windows Integration

### Autostart Configuration
The application can automatically start with Windows by modifying the registry. This is controlled through:
- Configuration file setting (`autostart`)
- Application settings interface

### System Tray
- A minimal interface in a system tray
- Right-click a menu for quick access
- Application continues running when the main window is closed


## Technical Details

### Architecture
- Multithreaded design for concurrent monitoring
- Event-driven GUI using CustomTkinter
- Process detection via psutil library
- Configuration management with configparser

### Process Monitoring
- Continuous scanning for new processes
- Real-time tracking of selected processes
- Automatic cleanup of terminated processes
- Filtering of system processes

## License

This project is licensed under the MIT License.
