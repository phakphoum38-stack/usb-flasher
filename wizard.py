import tkinter as tk
from tkinter import filedialog, messagebox
import threading

from flasher.efi import build_efi
from flasher.hardware import get_hw
from flasher.verify import verify_flash
from flasher.core import flash_image
from flasher.formats import prepare_image
from flasher.devices import get_usb_devices
from flasher.autofix import validate_and_fix
from flasher.cloud import cloud_fix

state = {
    "image": "",
    "device": "",
    "hw": None,
    "efi_dir": "build_efi"
}

root = tk.Tk()
root.title("Hackintosh Wizard")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

def clear():
    for w in frame.winfo_children():
        w.destroy()

# STEP 1
def step1():
    clear()
    tk.Label(frame, text="Step 1: Select macOS Image").pack()

    def browse():
        path = filedialog.askopenfilename()
        state["image"] = path
        label.config(text=path)

    tk.Button(frame, text="Browse", command=browse).pack()
    label = tk.Label(frame, text="No file")
    label.pack()

    tk.Button(frame, text="Next", command=step2).pack()

# STEP 2
def step2():
    clear()
    tk.Label(frame, text="Step 2: Select USB").pack()

    devices = get_usb_devices()

    listbox = tk.Listbox(frame)
    listbox.pack(fill="both", expand=True)

    for d in devices:
        listbox.insert(tk.END, f"{d['path']} | {d['model']}")

    def select():
        idx = listbox.curselection()[0]
        state["device"] = devices[idx]["path"]
        step3()

    tk.Button(frame, text="Next", command=select).pack()

# STEP 3
def step3():
    clear()
    tk.Label(frame, text="Step 3: Analyze Hardware").pack()

    hw = get_hw()
    state["hw"] = hw

    tk.Label(frame, text=str(hw)).pack()
    tk.Button(frame, text="Next", command=step4).pack()

# STEP 4 (BUILD + FLASH)
def step4():
    clear()
    tk.Label(frame, text="Step 4: Build + Flash").pack()

    status = tk.Label(frame, text="Idle")
    status.pack()

    def run():
        try:
            img = prepare_image(state["image"])
            build_efi(state["efi_dir"], "OpenCore")

            flash_image(img, state["device"])
            verify_flash(img, state["device"])

            ok = validate_and_fix(state["efi_dir"], state["hw"])

            if not ok:
                status.config(text="Trying cloud fix...")
                cloud_fix(state["efi_dir"], state["hw"])

            status.config(text="Done 🎉")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Start", command=lambda: threading.Thread(target=run).start()).pack()

# start
step1()
root.mainloop()
