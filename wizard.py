import tkinter as tk
from tkinter import filedialog, messagebox
import threading

from flasher.efi import build_efi
from flasher.hardware import get_hw
from flasher.verify import verify_flash
from flasher.core import flash_image
from flasher.formats import prepare_image
from flasher.devices import get_usb_devices
from flasher.safety import check_device
from flasher.progress import ProgressEmitter


state = {
    "image": "",
    "device": "",
    "hw": None,
    "efi_dir": "build_efi"
}

root = tk.Tk()
root.title("USB Flasher Wizard (Stable)")
root.geometry("600x450")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)


def clear():
    for w in frame.winfo_children():
        w.destroy()


# =========================
# STEP 1
# =========================
def step1():
    clear()
    tk.Label(frame, text="Step 1: Select Image").pack()

    def browse():
        path = filedialog.askopenfilename()
        state["image"] = path
        label.config(text=path)

    tk.Button(frame, text="Browse", command=browse).pack()
    label = tk.Label(frame, text="No file")
    label.pack()

    tk.Button(frame, text="Next", command=step2).pack()


# =========================
# STEP 2
# =========================
def step2():
    clear()
    tk.Label(frame, text="Step 2: Select USB").pack()

    devices = get_usb_devices()

    listbox = tk.Listbox(frame)
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
# STEP 3
# =========================
def step3():
    clear()
    tk.Label(frame, text="Step 3: Hardware Check").pack()

    hw = get_hw()
    state["hw"] = hw

    tk.Label(frame, text=str(hw)).pack()

    tk.Button(frame, text="Next", command=step4).pack()


# =========================
# STEP 4 (FLASH)
# =========================
def step4():
    clear()

    tk.Label(frame, text="Step 4: Flash").pack()

    status = tk.Label(frame, text="Idle")
    status.pack()

    def run():
        try:
            if not state["image"]:
                raise Exception("No image selected")

            if not state["device"]:
                raise Exception("No USB selected")

            # 🛑 SAFETY
            check_device(state["device"])

            img = prepare_image(state["image"])

            status.config(text="Building EFI...")
            build_efi(state["efi_dir"], "OpenCore")

            status.config(text="Flashing...")

            flash_image(img, state["device"])

            status.config(text="Verifying...")

            verify_flash(img, state["device"])

            status.config(text="DONE ✅")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            status.config(text="FAILED ❌")

    tk.Button(frame, text="START", bg="green", fg="white",
              command=lambda: threading.Thread(target=run, daemon=True).start()).pack()


step1()
root.mainloop()
