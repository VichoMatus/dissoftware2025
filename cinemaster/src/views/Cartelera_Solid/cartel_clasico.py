from .cartel_base import CartelBase
from PIL import Image, ImageTk
import customtkinter as ctk
import os

class CartelClasico(CartelBase):
    def create_widgets(self):
        image_path = self.pelicula.Image_path if self.pelicula.Image_path else os.path.abspath("cinemaster/src/views/images/default.jpg")
        try:
            pil_image = Image.open(image_path)
            pil_image = pil_image.resize((160, 160))
            self.img = ImageTk.PhotoImage(pil_image)
        except:
            self.img = ImageTk.PhotoImage(Image.open("cinemaster/src/views/images/default.jpg").resize((160, 160)))

        image_label = ctk.CTkLabel(self, image=self.img, text="")
        image_label.image = self.img
        image_label.pack(pady=10)

        info_label = ctk.CTkLabel(
            self,
            text=f"Nombre: {self.pelicula.Title}\nGénero: {self.pelicula.Gender}\nDuración: {self.pelicula.Duration} min",
            text_color="white",
            font=("Arial", 12),
            wraplength=160
        )
        info_label.pack(pady=5)

        showtimes_with_ids = [(h.id, h.fecha) for h in self.pelicula.horarios]
        showtimes_with_ids.sort(key=lambda x: x[1])
        reserve_button = ctk.CTkButton(
            self,
            text="Reservar",
            command=lambda: self.reserve_callback(self.pelicula, showtimes_with_ids, self.cliente)
        )
        reserve_button.pack(pady=10)