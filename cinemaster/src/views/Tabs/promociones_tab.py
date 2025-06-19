import customtkinter as ctk
from tkinter import ttk

class PromocionesTab(ctk.CTkFrame):
    def __init__(self, parent, promociones_service):
        super().__init__(parent)
        self.promociones_service = promociones_service

        ctk.CTkLabel(self, text="Gestor de Promociones", font=("Arial", 16, "bold")).pack(pady=10)
        columnas = ("ID", "Nombre", "Descuento", "Activa")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(padx=10, pady=10, fill="x")