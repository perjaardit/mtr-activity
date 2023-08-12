import tkinter as tk

from PIL import Image, ImageTk


class ImageShield:

    def __init__(self):
        self.window = None
        self.image_path = 'images/yubikey-5-nfc.png'

    def put_shield(self):
        if self.window:
            # Shield already present, do nothing
            return

        # Create a transparent top-level window
        self.window = self.add_shield()

    def add_shield(self):
        # Create a Tkinter window
        root = tk.Tk()
        root.attributes("-fullscreen", True)
        root.configure(background="black")
        root.overrideredirect(True)

        # Load the shield image
        shield_image = Image.open(self.image_path)
        shield_image = shield_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))

        # Convert the image to Tkinter format
        shield_photo = ImageTk.PhotoImage(shield_image)

        # Create a label and display the shield image
        label = tk.Label(root, image=shield_photo)
        label.pack(fill=tk.BOTH, expand=tk.YES)

        # Update the window to show the shield image
        root.update()

        # Return the root window object
        return root

    def remove_shield(self):
        if self.window:
            self.window.destroy()
            self.window = None
