from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secret Image Messenger")
        self.root.geometry("700x500")
        
        # GUI Elements
        Label(root, text="Image Steganography Tool", font=("Arial", 16)).pack(pady=10)
        
        # Image Display Frame
        self.img_frame = Frame(root)
        self.img_frame.pack(pady=20)
        
        # Buttons
        Button(root, text="Upload Image", command=self.upload_image).pack(pady=5)
        Button(root, text="Hide Message", command=self.hide_message).pack(pady=5)
        Button(root, text="Extract Message", command=self.extract_message).pack(pady=5)
        
        # Text Input
        self.message = Text(root, height=5, width=50)
        self.message.pack(pady=10)
        
        # Variables
        self.image_path = ""
        self.original_image = None
        self.tk_image = None
        self.image_label = Label(self.img_frame)
        self.image_label.pack()

    def upload_image(self):
        filetypes = (("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*"))
        self.image_path = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        
        if self.image_path:
            try:
                self.original_image = Image.open(self.image_path)
                self.display_image()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def display_image(self):
        # Resize for display while maintaining aspect ratio
        max_size = (400, 400)
        img = self.original_image.copy()
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)
        self.image_label.image = self.tk_image  # Keep reference

    def hide_message(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return
            
        secret_msg = self.message.get("1.0", END).strip()
        if not secret_msg:
            messagebox.showwarning("Warning", "Please enter a message to hide!")
            return
            
        try:
            # Add termination marker
            secret_msg += "====END===="
            
            output_path = filedialog.asksaveasfilename(
                defaultextension=".png"".jpeg"".jpg",
                filetypes=[(".png","*.png")],
                title="Save modified image"
            )
            
            if output_path:
                self.lsb_encode(self.image_path, secret_msg, output_path)
                messagebox.showinfo("Success", "Message hidden successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to hide message: {str(e)}")

    def lsb_encode(self, image_path, secret_msg, output_path):
        img = Image.open(image_path)
        binary_msg = ''.join(format(ord(i), '08b') for i in secret_msg)
        
        if len(binary_msg) > img.width * img.height * 3:
            raise ValueError("Message too large for image!")
        
        pixels = list(img.getdata())
        new_pixels = []
        msg_index = 0
        
        for pixel in pixels:
            if msg_index < len(binary_msg):
                new_pixel = []
                for value in pixel[:3]:  # RGB channels only
                    if msg_index < len(binary_msg):
                        # Clear LSB and set to message bit
                        new_value = (value & ~1) | int(binary_msg[msg_index])
                        new_pixel.append(new_value)
                        msg_index += 1
                    else:
                        new_pixel.append(value)
                # Keep alpha channel if exists
                if len(pixel) == 4:
                    new_pixel.append(pixel[3])
                new_pixels.append(tuple(new_pixel))
            else:
                new_pixels.append(pixel)
        
        new_img = Image.new(img.mode, img.size)
        new_img.putdata(new_pixels)
        new_img.save(output_path, "png")

    def extract_message(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return
            
        try:
            hidden_msg = self.lsb_decode(self.image_path)
            self.message.delete("1.0", END)
            self.message.insert("1.0", hidden_msg)
            messagebox.showinfo("Extracted Message", f"Hidden message found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract message: {str(e)}")

    def lsb_decode(self, image_path):
        img = Image.open(image_path)
        binary_msg = ""
        
        for pixel in img.getdata():
            for value in pixel[:3]:  # Read RGB channels
                binary_msg += str(value & 1)
        
        # Convert binary to string
        message = ""
        for i in range(0, len(binary_msg), 8):
            byte = binary_msg[i:i+8]
            message += chr(int(byte, 2))
            if message.endswith("====END===="):
                return message[:-11]
        
        return "No hidden message found or message corrupted"

if __name__ == "__main__":
    root = Tk()
    app = StegoApp(root)
    root.mainloop()