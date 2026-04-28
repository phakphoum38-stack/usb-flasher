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
from flasher.progress import ProgressEmitter
from flasher.safety import check_device

# =========================
# STATE
# =========================
state = {
    "image": "",
    "device": "",
    "hw": None,
    "efi_dir": "build_efi",
    "progress": 0
}

# =========================
# UI ROOT
# =========================
root = tk.Tk()
root.title("Hackintosh Wizard Pro")
root.geometry("600x500")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

progress_var = tk.IntVar()


# =========================
# CLEAR UI
# =========================
def clear():
    for w in frame.winfo_children():
        w.destroy()


# =========================
# STEP 1 - IMAGE
# =========================
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

    def next():
        if not state["image"]:
            messagebox.showerror("Error", "Select image first")
            return
        step2()

    tk.Button(frame, text="Next", command=next).pack()


# =========================
# STEP 2 - USB
# =========================
def step2():
    clear()

    tk.Label(frame, text="Step 2: Select USB Device").pack()

    devices = get_usb_devices()

    listbox = tk.Listbox(frame, height=8)
    listbox.pack(fill="both", expand=True)

    for d in devices:
        listbox.insert(tk.END, f"{d['path']} | {d['model']}")

    def select():
        if not listbox.curselection():
            messagebox.showerror("Error", "Select USB first")
            return

        idx = listbox.curselection()[0]
        state["device"] = devices[idx]["path"]

        step3()

    tk.Button(frame, text="Next", command=select).pack()


# =========================
# STEP 3 - HARDWARE
# =========================
def step3():
    clear()

    tk.Label(frame, text="Step 3: Hardware Analysis").pack()

    hw = get_hw()
    state["hw"] = hw

    tk.Label(frame, text=str(hw)).pack()

    tk.Button(frame, text="Next", command=step4).pack()


# =========================
# STEP 4 - FLASH + BUILD
# =========================
def step4():
    clear()

    tk.Label(frame, text="Step 4: Build & Flash").pack()

    progress = tk.Scale(frame, from_=0, to=100, orient="horizontal",
                        variable=progress_var)
    progress.pack(fill="x")

    status = tk.Label(frame, text="Idle")
    status.pack()

    def update_progress(val):
        progress_var.set(val)
        root.update_idletasks()

    # =========================
    # MAIN PROCESS
    # =========================
    def run():
        try:
            img = prepare_image(state["image"])

            # 🧠 EFI BUILD
            build_efi(state["efi_dir"], "OpenCore")

            # 🛑 SAFETY CHECK
            check_device(state["device"])

            status.config(text="Flashing...")

            # ⚡ PROGRESS EMITTER
            emitter = ProgressEmitter(callback=update_progress)
            emitter.start()

            flash_image(img, state["device"])

            status.config(text="Verifying...")
            verify_flash(img, state["device"])

            ok = validate_and_fix(state["efi_dir"], state["hw"])

            if not ok:
                status.config(text="Cloud fixing...")
                cloud_fix(state["efi_dir"], state["hw"])

            status.config(text="Done 🎉")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            status.config(text="Failed ❌")

    tk.Button(frame, text="START FLASH", bg="green", fg="white",
              command=lambda: threading.Thread(target=run, daemon=True).start()).pack()


# =========================
# START
# =========================
step1()
root.mainloop()
