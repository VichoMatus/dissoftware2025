import customtkinter as ctk
from PIL import Image, ImageTk
import os

class HeaderBar(ctk.CTkFrame):
    def __init__(self, parent, employee_name):
        super().__init__(parent, height=60)

        logo_label = ctk.CTkLabel(self, text="[Logo]")
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "..", "images", "logo.png")
            logo_path = os.path.abspath(logo_path)
            logo_image = Image.open(logo_path).resize((100, 100))
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label.configure(image=self.logo_photo, text="")
        except Exception:
            pass

        logo_label.pack(side="left", padx=10)

        ctk.CTkLabel(self, text="Gestión Empleado", font=("Arial", 20, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(self, text=f"Bienvenido, {employee_name.capitalize()}", font=("Arial", 20, "bold")).pack(side="right", padx=10)