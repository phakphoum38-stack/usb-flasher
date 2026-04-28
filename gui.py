import tkinter as tk
from tkinter import filedialog, messagebox
import threading

from flasher.devices import get_usb_devices
from flasher.core import flash_image
from flasher.verify import verify_flash
from flasher.formats import prepare_image
from flasher.safety import check_device

devices = []
selected_device = None


# =========================
# 📂 SELECT IMAGE
# =========================
def browse():
    path = filedialog.askopenfilename()
    file_label.config(text=path)


# =========================
# 🔍 LOAD USB
# =========================
def load_devices():
    global devices
    devices = get_usb_devices()

    device_list.delete(0, tk.END)

    for d in devices:
        device_list.insert(tk.END, f"{d['path']} | {d['model']}")


# =========================
# 📌 SELECT DEVICE
# =========================
def select(evt):
    global selected_device

    if not device_list.curselection():
        return

    selected_device = devices[device_list.curselection()[0]]["path"]
    status.config(text=f"Selected: {selected_device}")


# =========================
# ⚡ FLASH CORE
# =========================
def flash():
    def run():
        try:
            img_path = file_label.cget("text")

            if not img_path or img_path == "No file":
                messagebox.showerror("Error", "No image selected")
                return

            if not selected_device:
                messagebox.showerror("Error", "No USB selected")
                return

            # 🛑 SAFETY CHECK
            check_device(selected_device)

            img = prepare_image(img_path)

            status.config(text="Flashing...")

            # ⚡ FLASH
            flash_image(img, selected_device)

            status.config(text="Verifying...")

            verify_flash(img, selected_device)

            status.config(text="Done ✅")

        except Exception as e:
            messagebox.showerror("Flash Error", str(e))
            status.config(text="Failed ❌")

    threading.Thread(target=run, daemon=True).start()


# =========================
# 🖥 UI
# =========================
root = tk.Tk()
root.title("USB Flasher Pro")
root.geometry("520x450")


tk.Label(root, text="Select Image").pack()
tk.Button(root, text="Browse", command=browse).pack()

file_label = tk.Label(root, text="No file")
file_label.pack()


tk.Button(root, text="Load USB Devices", command=load_devices).pack()


device_list = tk.Listbox(root, height=8)
device_list.pack(fill="both", expand=True)
device_list.bind("<<ListboxSelect>>", select)


tk.Button(root, text="FLASH", bg="green", fg="white", command=flash).pack(pady=10)

status = tk.Label(root, text="Idle")
status.pack()

root.mainloop()
