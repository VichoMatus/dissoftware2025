import customtkinter as ctk
from tkinter import ttk

class FuncionesTab(ctk.CTkFrame):
    def __init__(self, parent, funcion_service):
        super().__init__(parent)
        self.funcion_service = funcion_service

        ctk.CTkLabel(self, text="Gestor de Funciones", font=("Arial", 16, "bold")).pack(pady=10)
        columnas = ("ID", "Película", "Empleado", "Horario")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(padx=10, pady=10, fill="x")