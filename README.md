# SystemBootInfo

⚠ **Warning:** This application must be run as **Administrator** to correctly fetch boot duration.  
⚠ Executable location: `dist/main.exe`

---

## Overview

**System Boot Info** is a lightweight Python application that displays your system's boot time, uptime, and the exact boot duration in seconds. It uses:

- **WMI** (`wmi` Python module) to fetch the system boot time and calculate uptime.
- **PowerShell** to query the Windows Event Log for the last boot duration (Event ID 100 in `Microsoft-Windows-Diagnostics-Performance/Operational` log).
- **Tkinter** to provide a modern, minimal, always-on-top GUI.

---

## How It Works

1. **Boot Time & Uptime:**
   - Uses `wmi.Win32_OperatingSystem()` to get the last boot time.
   - Calculates the uptime by comparing the last boot time with the current system time.

2. **Boot Duration:**
   - Executes a PowerShell command to fetch the most recent boot performance event.
   - Converts the value to seconds for display.

3. **GUI:**
   - Tkinter-based card-style window.
   - Shows boot time, uptime, and boot duration.
   - Includes **Refresh** and **Close** buttons.
   - Always appears on top of other windows and positioned at the bottom-right corner.

---

## Example Usage

Run the executable:

```powershell
dist\main.exe
Or, if you want to run the Python script directly (Python 3.12+ required):

powershell
python main.py

