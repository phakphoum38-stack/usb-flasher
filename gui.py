import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import threading

from flasher.devices import get_usb_devices
from flasher.core import flash_image
from flasher.verify import verify_flash
from flasher.formats import prepare_image
from flasher.efi import generate_config

devices = []
selected_device = None

def browse():
    path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, path)

def load_devices():
    global devices
    devices = get_usb_devices()
    listbox.delete(0, tk.END)

    for d in devices:
        listbox.insert(tk.END, f"{d['path']} | {d['model']}")

def select_device(evt):
    global selected_device
    idx = listbox.curselection()[0]
    selected_device = devices[idx]["path"]

def run_flash():
    try:
        img = prepare_image(entry.get())
        flash_image(img, selected_device)
        verify_flash(img, selected_device)
        messagebox.showinfo("Done", "Flash complete")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def start_flash():
    if not selected_device:
        messagebox.showerror("Error", "Select device")
        return

    threading.Thread(target=run_flash).start()

def build_efi():
    folder = filedialog.askdirectory()
    if folder:
        generate_config(folder)
        messagebox.showinfo("EFI", "Config generated")

# UI
root = tk.Tk()
root.title("USB Flasher Pro")

entry = tk.Entry(root, width=50)
entry.pack()

tk.Button(root, text="Browse", command=browse).pack()
tk.Button(root, text="Load USB", command=load_devices).pack()

listbox = tk.Listbox(root)
listbox.pack()
listbox.bind("<<ListboxSelect>>", select_device)

progress = Progressbar(root, length=300)
progress.pack()

tk.Button(root, text="Flash", command=start_flash).pack()
tk.Button(root, text="Generate EFI", command=build_efi).pack()

root.mainloop()
