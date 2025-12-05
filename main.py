import tkinter as tk
from datetime import datetime
import wmi
import subprocess

# ---------------- PowerShell Boot Duration ----------------
def get_boot_duration():
    try:
        ps_cmd = r"""
        $e = Get-WinEvent -FilterXPath "*[System/EventID=100]" -LogName "Microsoft-Windows-Diagnostics-Performance/Operational" -MaxEvents 1;
        ($e.Properties[6].Value + $e.Properties[7].Value) / 1000
        """

        result = subprocess.check_output(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        ).strip()

        if not result or "null" in result.lower():
            return "⚠ Boot record not found"

        result = result.replace(",", ".")  # virgülü noktaya çevir
        duration = float(result)

        return f"⚡ Boot Duration: {duration:.2f} seconds"

    except Exception as e:
        return f"⚠ Could not fetch boot duration: {e}"


# ---------------- System Uptime ----------------
def get_system_info():
    try:
        c = wmi.WMI()
        for os in c.Win32_OperatingSystem():
            boot_str = os.LastBootUpTime.split('.')[0]
            boot_time = datetime.strptime(boot_str, '%Y%m%d%H%M%S')

        now = datetime.now()
        uptime = now - boot_time
        days = uptime.days
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60

        boot_duration = get_boot_duration()

        return (
            f"📅 Boot Time: {boot_time.strftime('%d.%m.%Y %H:%M:%S')}\n"
            f"⏱ Uptime: {days} days {hours} hours {minutes} minutes\n"
            f"{boot_duration}"
        )

    except Exception as e:
        return f"⚠ Error: {str(e)}"

# ---------------- GUI ----------------
def show_gui():
    info_text = get_system_info()
    width, height = 400, 180

    root = tk.Tk()
    root.title("System Boot Info")
    root.configure(bg="#f0f2f5")
    root.attributes("-topmost", True)

    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = sw - width - 20, sh - height - 60
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)

    # Main card frame
    card = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)
    card.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Header
    header = tk.Frame(card, bg="#2c3e50", height=40)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    header_label = tk.Label(header, text="System Boot Info", font=("Segoe UI", 12, "bold"),
                            fg="white", bg="#2c3e50")
    header_label.pack(side=tk.LEFT, padx=10, pady=5)

    # Content
    content = tk.Frame(card, bg="white", padx=15, pady=10)
    content.pack(fill=tk.BOTH, expand=True)
    info_label = tk.Label(content, text=info_text, font=("Consolas", 11),
                          bg="white", fg="#2c3e50", justify=tk.LEFT, anchor="w")
    info_label.pack(fill=tk.BOTH, expand=True)

    # Buttons
    button_frame = tk.Frame(content, bg="white")
    button_frame.pack(fill=tk.X, pady=(10,0))

    def refresh():
        info_label.config(text=get_system_info())

    refresh_btn = tk.Button(button_frame, text="🔄 Refresh", bg="#3498db", fg="white",
                            font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=10, pady=5,
                            command=refresh)
    refresh_btn.pack(side=tk.LEFT, padx=5)

    close_btn = tk.Button(button_frame, text="✕ Close", bg="#e74c3c", fg="white",
                          font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=10, pady=5,
                          command=root.destroy)
    close_btn.pack(side=tk.RIGHT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    show_gui()
