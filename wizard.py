import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import ctypes
import os
import time
from datetime import datetime

from flasher.devices import get_usb_devices
from flasher.safety import safety_pipeline
from flasher.rust_core import flash_with_rust
from flasher.verify import quick_verify
from flasher.formats import prepare_image
from flasher.updater import check_update, download_update, run_update
from flasher.crash_report import send_crash
from flasher.config import load_config

# =========================
# VERSION
# =========================
def get_version():
    try:
        with open("VERSION") as f:
            return f.read().strip()
    except:
        return "1.0.0"

APP_VERSION = get_version()

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(f"USB Flash Tool Pro v{APP_VERSION}")
        self.root.geometry("720x540")

        self.cfg = load_config()

        self.image = ""
        self.device = None
        self.devices = []
        self.running = False

        self.last_update = 0
        self.start_time = 0

        self.build_ui()
        self.auto_load()
        self.check_updates()

    # =========================
    # LOG
    # =========================
    def log(self, msg):
        path = os.path.join(LOG_DIR, "latest.log")

        if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
            try:
                os.replace(path, os.path.join(LOG_DIR, "old.log"))
            except:
                pass

        t = datetime.now().strftime("%H:%M:%S")
        line = f"[{t}] {msg}\n"

        self.root.after(0, lambda: (
            self.logbox.insert(tk.END, line),
            self.logbox.see(tk.END)
        ))

        with open(path, "a", encoding="utf-8") as f:
            f.write(line)

    # =========================
    # AUTO USB
    # =========================
    def auto_load(self):
        self.devices = get_usb_devices()
        self.listbox.delete(0, tk.END)

        for d in self.devices:
            self.listbox.insert(tk.END, f"{d['path']} | {d['model']}")

        self.log("USB auto-detected")

    # =========================
    # UPDATE
    # =========================
    def check_updates(self):
        if not self.cfg.get("auto_update"):
            return
        try:
            data = check_update(APP_VERSION)
            if data:
                if messagebox.askyesno("Update", "New version available. Update now?"):
                    path = download_update(data)
                    if path:
                        run_update(path)
        except:
            pass

    # =========================
    # UI
    # =========================
    def build_ui(self):
        tk.Label(self.root, text=f"USB Flash Tool Pro v{APP_VERSION}", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.root, text="Select Image", command=self.select_image).pack()

        self.file_label = tk.Label(self.root, text="No file")
        self.file_label.pack()

        tk.Button(self.root, text="Refresh USB", command=self.auto_load).pack()

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.select_device)

        self.pb = ttk.Progressbar(self.root, length=500, maximum=100)
        self.pb.pack(pady=10)

        self.status = tk.Label(self.root, text="Idle")
        self.status.pack()

        self.flash_btn = tk.Button(self.root, text="FLASH", bg="green", command=self.start)
        self.flash_btn.pack(pady=5)

        self.cancel_btn = tk.Button(self.root, text="CANCEL", bg="red", command=self.cancel)
        self.cancel_btn.pack()
        self.cancel_btn.config(state="disabled")

        self.logbox = tk.Text(self.root, height=8)
        self.logbox.pack(fill="both", expand=True)

    # =========================
    # SELECT IMAGE
    # =========================
    def select_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.image = path
            self.file_label.config(text=path)
            self.log(f"Image: {path}")

    # =========================
    # SELECT DEVICE
    # =========================
    def select_device(self, e):
        if not self.listbox.curselection():
            return
        idx = self.listbox.curselection()[0]
        self.device = self.devices[idx]["path"]
        self.log(f"Device: {self.device}")

    # =========================
    # CANCEL
    # =========================
    def cancel(self):
        self.running = False
        self.pb['value'] = 0
        self.status.config(text="Cancelled")
        self.flash_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.log("Cancelled")

    # =========================
    # START
    # =========================
    def start(self):
        if not is_admin():
            messagebox.showerror("Error", "Run as admin")
            return

        if not self.image or not self.device:
            messagebox.showerror("Error", "Select image + USB")
            return

        if not messagebox.askyesno("Confirm", f"Flash {self.device} ?"):
            return

        self.start_time = time.time()

        def progress(p, s):
            if not self.running:
                return

            now = time.time()
            if now - self.last_update < 0.05:
                return

            self.last_update = now

            elapsed = now - self.start_time
            eta = int((100 - p) * (elapsed / p)) if p > 0 else 0

            self.root.after(0, lambda: (
                self.pb.config(value=p),
                self.status.config(text=f"{p}% | ETA {eta}s")
            ))

        def run():
            try:
                self.running = True
                self.flash_btn.config(state="disabled")
                self.cancel_btn.config(state="normal")

                self.log("Safety check...")
                safety_pipeline(self.device)

                # 🔥 FIX ISO/DMG
                self.log("Preparing image...")
                img = prepare_image(self.image)
                self.log(f"Using: {img}")

                self.log("Flashing...")
                flash_with_rust(img, self.device, progress)

                if not self.running:
                    return

                self.log("Verifying...")
                ok = quick_verify(img, self.device)

                if ok:
                    self.status.config(text="Done")
                    self.log("SUCCESS")
                    messagebox.showinfo("OK", "Flash done")
                else:
                    raise Exception("Verify failed")

            except Exception as e:
                send_crash(e)
                self.log(f"ERROR: {e}")
                messagebox.showerror("Error", str(e))

            finally:
                self.running = False
                self.flash_btn.config(state="normal")
                self.cancel_btn.config(state="disabled")

        threading.Thread(target=run, daemon=True).start()


root = tk.Tk()
app = App(root)
root.mainloop()
