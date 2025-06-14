import customtkinter as ctk

class MovieInfoWidget(ctk.CTkLabel):
    def __init__(self, parent, title, gender, duration):
        info = f"Título: {title}\nGénero: {gender}\nDuración: {duration} min"
        super().__init__(parent, text=info, font=("Arial", 14), justify="left")