import tkinter as tk

from tkinter import filedialog, messagebox

import threading

from flasher.devices import get_usb_devices

from flasher.core import flash_image

from flasher.formats import prepare_image

class App:

    def __init__(self, root):

        self.root = root

        self.root.title("USB Flash Tool Pro")

        self.root.geometry("600x400")

        self.image_path = ""

        self.device = None

        self.build_ui()

    def build_ui(self):

        tk.Label(self.root, text="USB Flash Tool Pro", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.root, text="Select Image", command=self.select_image).pack()

        self.file_label = tk.Label(self.root, text="No file selected")

        self.file_label.pack()

        tk.Button(self.root, text="Load USB Devices", command=self.load_devices).pack()

        self.listbox = tk.Listbox(self.root)

        self.listbox.pack(fill="both", expand=True)

        self.listbox.bind("<<ListboxSelect>>", self.select_device)

        self.progress = tk.Label(self.root, text="Idle")

        self.progress.pack()

        tk.Button(self.root, text="FLASH", bg="green", fg="white", command=self.start_flash).pack(pady=10)

    def select_image(self):

        self.image_path = filedialog.askopenfilename()

        self.file_label.config(text=self.image_path)

    def load_devices(self):

        self.devices = get_usb_devices()

        self.listbox.delete(0, tk.END)

        for d in self.devices:

            self.listbox.insert(tk.END, f"{d['path']} | {d['model']}")

    def select_device(self, evt):

        idx = self.listbox.curselection()[0]

        self.device = self.devices[idx]["path"]

    def start_flash(self):

        def run():

            try:

                self.progress.config(text="Preparing image...")

                img = prepare_image(self.image_path)

                self.progress.config(text="Flashing...")

                flash_image(img, self.device)

                self.progress.config(text="Done!")

                messagebox.showinfo("Success", "Flash completed!")

            except Exception as e:

                messagebox.showerror("Error", str(e))

        threading.Thread(target=run).start()

root = tk.Tk()

app = App(root)

root.mainloop()
