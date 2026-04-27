import tkinter as tk
from tkinter import filedialog
from flasher.core import flash_image

def select_file():
    path = filedialog.askopenfilename()
    entry.insert(0, path)

def start_flash():
    image = entry.get()
    device = device_entry.get()
    flash_image(image, device)

root = tk.Tk()
root.title("USB Flasher")

entry = tk.Entry(root, width=40)
entry.pack()

tk.Button(root, text="Browse", command=select_file).pack()

device_entry = tk.Entry(root)
device_entry.pack()

tk.Button(root, text="Flash", command=start_flash).pack()

root.mainloop()
