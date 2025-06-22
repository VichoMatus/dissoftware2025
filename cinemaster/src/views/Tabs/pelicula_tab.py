import customtkinter as ctk
from tkinter import ttk
from models.database import SessionLocal

class PeliculasTab(ctk.CTkFrame):
    def __init__(self, parent, pelicula_service):
        super().__init__(parent)
        self.pelicula_service = pelicula_service

        self.label = ctk.CTkLabel(self, text="Lista de Películas", font=("Arial", 20))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Título", "Duración", "Género", "Imagen"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Duración", text="Duración")
        self.tree.heading("Género", text="Género")
        self.tree.heading("Imagen", text="Imagen")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.reload_button = ctk.CTkButton(self, text="Cargar Películas", command=self.cargar_datos)
        self.reload_button.pack(pady=5)

        self.cargar_datos()

    def cargar_datos(self):
        db = SessionLocal()
        try:
            peliculas = self.pelicula_service.listar_peliculas(db)
            for item in self.tree.get_children():
                self.tree.delete(item)
            for pelicula in peliculas:
                self.tree.insert("", "end", values=(
                    pelicula.id_pelicula,
                    pelicula.Title,
                    pelicula.Duration,
                    pelicula.Gender,
                    pelicula.Image_path
                ))
        finally:
            db.close()