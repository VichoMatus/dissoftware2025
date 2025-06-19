import customtkinter as ctk
from tkinter import ttk

class PeliculasTab(ctk.CTkFrame):
    def __init__(self, parent, pelicula_service):
        super().__init__(parent)
        self.pelicula_service = pelicula_service

        ctk.CTkLabel(self, text="Gestor de Películas", font=("Arial", 16, "bold")).pack(pady=10)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        self.listado_tab = self.tabview.add("Listado")
        self.crear_tab = self.tabview.add("Crear")