import tkinter as tk
from tkinter import filedialog, messagebox

from flasher.devices import get_usb_devices
from flasher.core import flash_image
from flasher.verify import verify_flash
from flasher.formats import prepare_image
from flasher.efi import build_efi

selected_device = None

def select_image():
    path = filedialog.askopenfilename()
    image_entry.delete(0, tk.END)
    image_entry.insert(0, path)

def load_devices():
    global devices
    devices = get_usb_devices()
    listbox.delete(0, tk.END)

    for d in devices:
        listbox.insert(tk.END, f"{d['path']} | {d['model']} | {d['size']}")

def choose_device(event):
    global selected_device
    index = listbox.curselection()[0]
    selected_device = devices[index]["path"]

def start_flash():
    if not selected_device:
        messagebox.showerror("Error", "Select device first")
        return

    image = image_entry.get()

    if not image:
        messagebox.showerror("Error", "Select image")
        return

    try:
        img = prepare_image(image)
        flash_image(img, selected_device)
        verify_flash(img, selected_device)

        messagebox.showinfo("Done", "Flash complete!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def generate_efi():
    folder = filedialog.askdirectory()
    opencore = filedialog.askdirectory(title="Select OpenCore folder")

    if folder and opencore:
        build_efi(folder, opencore)
        messagebox.showinfo("EFI", "EFI generated!")


# ================= UI =================

root = tk.Tk()
root.title("USB Flasher Pro")

tk.Label(root, text="Image").pack()
image_entry = tk.Entry(root, width=50)
image_entry.pack()

tk.Button(root, text="Browse", command=select_image).pack()

tk.Button(root, text="Load USB Devices", command=load_devices).pack()

listbox = tk.Listbox(root, width=60)
listbox.pack()
listbox.bind("<<ListboxSelect>>", choose_device)

tk.Button(root, text="Flash", command=start_flash).pack()

tk.Button(root, text="Generate EFI", command=generate_efi).pack()

root.mainloop()
