from PIL import Image, ImageTk
import customtkinter as ctk
import os

class MovieImageWidget(ctk.CTkLabel):
    def __init__(self, parent, image_path):
        img_path = image_path if image_path and os.path.exists(image_path) \
            else os.path.abspath(os.path.join(os.path.dirname(__file__), "../../images/default.jpg"))
        pil_image = Image.open(img_path)
        pil_image = pil_image.resize((200, 200))
        self.img = ImageTk.PhotoImage(pil_image)
        super().__init__(parent, image=self.img, text="")
        self.image = self.img  # Mantener referencia