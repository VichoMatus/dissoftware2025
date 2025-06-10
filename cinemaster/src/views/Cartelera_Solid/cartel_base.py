import customtkinter as ctk

class CartelBase(ctk.CTkFrame):
    def __init__(self, parent, pelicula, cliente, reserve_callback):
        super().__init__(parent, corner_radius=10, width=180, height=250)
        self.pelicula = pelicula
        self.cliente = cliente
        self.reserve_callback = reserve_callback
        self.create_widgets()

    def create_widgets(self):
        raise NotImplementedError("Debes implementar create_widgets en la subclase")