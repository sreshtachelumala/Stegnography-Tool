import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np

def encode_message_in_image(image_path, message, output_path):
    image = Image.open(image_path)
    image_array = np.array(image)

    message_binary = ''.join(format(ord(char), '08b') for char in message)
    message_length = len(message_binary)

    if message_length > image_array.size:
        raise ValueError("Message is too long to be hidden in this image.")

    data_index = 0
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            for k in range(image_array.shape[2]):
                if data_index < message_length:
                    image_array[i, j, k] = (image_array[i, j, k] & ~1) | int(message_binary[data_index])
                    data_index += 1

    encoded_image = Image.fromarray(image_array)
    encoded_image.save(output_path)
    return f"Message encoded and saved to {output_path}"

def decode_message_from_image(image_path):
    image = Image.open(image_path)
    image_array = np.array(image)

    message_binary = ''.join([str(pixel & 1) for pixel in image_array.flatten()])
    message_bytes = [message_binary[i:i+8] for i in range(0, len(message_binary), 8)]
    message = ''.join([chr(int(byte, 2)) for byte in message_bytes])
    message = message.split('\x00', 1)[0]
    return message

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography App")
        
        self.mode = tk.StringVar(value="encode")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Steganography Tool", font=("Arial", 16)).pack(pady=10)

        tk.Radiobutton(self.root, text="Encode", variable=self.mode, value="encode").pack(anchor=tk.W)
        tk.Radiobutton(self.root, text="Decode", variable=self.mode, value="decode").pack(anchor=tk.W)

        tk.Label(self.root, text="Select Image File:").pack(anchor=tk.W, pady=5)
        self.image_path_entry = tk.Entry(self.root, width=50)
        self.image_path_entry.pack(anchor=tk.W, padx=5)
        tk.Button(self.root, text="Browse", command=self.browse_image).pack(anchor=tk.W, padx=5, pady=5)

        tk.Label(self.root, text="Message:").pack(anchor=tk.W, pady=5)
        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack(anchor=tk.W, padx=5, pady=5)

        tk.Label(self.root, text="Output Image File (for encoding):").pack(anchor=tk.W, pady=5)
        self.output_path_entry = tk.Entry(self.root, width=50)
        self.output_path_entry.pack(anchor=tk.W, padx=5)
        tk.Button(self.root, text="Browse", command=self.browse_output).pack(anchor=tk.W, padx=5, pady=5)

        tk.Button(self.root, text="Execute", command=self.execute).pack(pady=10)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, file_path)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image Files", "*.png")])
        if file_path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, file_path)

    def execute(self):
        mode = self.mode.get()
        image_path = self.image_path_entry.get()
        if not image_path:
            messagebox.showerror("Error", "Please select an image file.")
            return

        try:
            if mode == "encode":
                message = self.message_entry.get()
                output_path = self.output_path_entry.get()
                if not message or not output_path:
                    messagebox.showerror("Error", "Please provide both message and output file path.")
                    return
                result = encode_message_in_image(image_path, message, output_path)
                messagebox.showinfo("Success", result)
            else:
                decoded_message = decode_message_from_image(image_path)
                messagebox.showinfo("Decoded Message", decoded_message)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
