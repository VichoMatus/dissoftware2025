from PIL import Image, ImageTk
import customtkinter as ctk
import os

class SeatImageWidget(ctk.CTkLabel):
    def __init__(self, parent, image_path):
        try:
            seat_image = Image.open(image_path)
            seat_image = seat_image.resize((500, 400))
            self.seat_image_tk = ImageTk.PhotoImage(seat_image)
            super().__init__(parent, image=self.seat_image_tk, text="")
            self.image = self.seat_image_tk  # Mantener referencia
        except Exception as e:
            print(f"Error al cargar la imagen de asientos: {e}")
            super().__init__(parent, text="No se pudo cargar la imagen")