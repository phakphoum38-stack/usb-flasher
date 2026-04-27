import tkinter as tk
from tkinter import filedialog
import threading

from flasher.devices import get_usb_devices
from flasher.core import flash_image
from flasher.verify import verify_flash
from flasher.formats import prepare_image

devices = []
selected_device = None

def browse():
    path = filedialog.askopenfilename()
    file_label.config(text=path)

def load_devices():
    global devices
    devices = get_usb_devices()
    device_list.delete(0, tk.END)

    for d in devices:
        device_list.insert(tk.END, f"{d['path']} | {d['model']}")

def select(evt):
    global selected_device
    selected_device = devices[device_list.curselection()[0]]["path"]

def flash():
    def run():
        img = prepare_image(file_label.cget("text"))
        status.config(text="Flashing...")
        flash_image(img, selected_device)
        verify_flash(img, selected_device)
        status.config(text="Done!")

    threading.Thread(target=run).start()

root = tk.Tk()
root.title("USB Flasher Pro")
root.geometry("500x400")

tk.Label(root, text="Select Image").pack()
tk.Button(root, text="Browse", command=browse).pack()

file_label = tk.Label(root, text="No file")
file_label.pack()

tk.Button(root, text="Load USB", command=load_devices).pack()

device_list = tk.Listbox(root)
device_list.pack(fill="both", expand=True)
device_list.bind("<<ListboxSelect>>", select)

tk.Button(root, text="FLASH", bg="green", fg="white", command=flash).pack()

status = tk.Label(root, text="Idle")
status.pack()

root.mainloop()
