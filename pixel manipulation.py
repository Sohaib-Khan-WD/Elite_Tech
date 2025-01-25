

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np


class ImageEncryptorDecryptor:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Image Encryptor & Decryptor")
        self.master.geometry("600x600")

        self.image = None
        self.image_path = None
        self.encrypted_image = None
        self.encryption_method = "Shift"
        self.swap_indices = None

        self.create_widgets()

    def create_widgets(self):
        image_operations_frame = tk.Frame(self.master)
        image_operations_frame.pack(pady=20)

        self.load_button = tk.Button(image_operations_frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=10)

        self.encrypt_button = tk.Button(image_operations_frame, text="Encrypt Image", command=self.encrypt_image, state=tk.DISABLED)
        self.encrypt_button.grid(row=0, column=1, padx=10)

        self.decrypt_button = tk.Button(image_operations_frame, text="Decrypt Image", command=self.decrypt_image, state=tk.DISABLED)
        self.decrypt_button.grid(row=0, column=2, padx=10)

        self.encryption_method_var = tk.StringVar(value=self.encryption_method)
        self.method_menu = ttk.Combobox(image_operations_frame, textvariable=self.encryption_method_var, 
                                         values=["Shift", "XOR", "Random Swap"])
        self.method_menu.grid(row=1, column=1, padx=10)
        self.method_menu.current(0)

        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(pady=20)

        self.canvas = tk.Canvas(self.canvas_frame, width=500, height=350, bg="gray")
        self.canvas.pack()

        self.status_label = tk.Label(self.master, text="Status: Ready", font=("Arial", 12))
        self.status_label.pack()

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.show_image(self.image)
            self.encrypt_button.config(state=tk.NORMAL)
            self.update_status("Image loaded successfully!")

    def show_image(self, image):
        image.thumbnail((500, 350))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def encrypt_image(self):
        if self.image:
            method = self.encryption_method_var.get()
            img_array = np.array(self.image)

            if method == "Shift":
                encrypted_array = img_array + 50
            elif method == "XOR":
                encrypted_array = img_array ^ 100
            elif method == "Random Swap":
                encrypted_array, self.swap_indices = self.random_pixel_swap(img_array)

            encrypted_array = np.clip(encrypted_array, 0, 255)
            self.encrypted_image = Image.fromarray(encrypted_array.astype(np.uint8))
            self.show_image(self.encrypted_image)
            self.decrypt_button.config(state=tk.NORMAL)
            self.update_status(f"Image encrypted using {method} method!")

    def decrypt_image(self):
        if self.encrypted_image:
            method = self.encryption_method_var.get()
            encrypted_array = np.array(self.encrypted_image)

            if method == "Shift":
                decrypted_array = encrypted_array - 50
            elif method == "XOR":
                decrypted_array = encrypted_array ^ 100
            elif method == "Random Swap" and self.swap_indices is not None:
                decrypted_array = self.reverse_random_swap(encrypted_array)

            decrypted_array = np.clip(decrypted_array, 0, 255)
            decrypted_image = Image.fromarray(decrypted_array.astype(np.uint8))
            self.show_image(decrypted_image)
            self.update_status(f"Image decrypted using {method} method!")
            self.decrypt_button.config(state=tk.DISABLED)
            self.encrypt_button.config(state=tk.NORMAL)

    def random_pixel_swap(self, img_array):
        flat_array = img_array.flatten()
        indices = np.arange(flat_array.size)
        np.random.shuffle(indices)
        self.swap_indices = indices
        shuffled_array = flat_array[indices]
        return shuffled_array.reshape(img_array.shape), self.swap_indices

    def reverse_random_swap(self, encrypted_array):
        if self.swap_indices is not None:
            flat_array = encrypted_array.flatten()
            reversed_array = np.zeros_like(flat_array)
            reversed_array[self.swap_indices] = flat_array
            return reversed_array.reshape(encrypted_array.shape)
        else:
            return encrypted_array


root = tk.Tk()
image_tool = ImageEncryptorDecryptor(root)
root.mainloop()
