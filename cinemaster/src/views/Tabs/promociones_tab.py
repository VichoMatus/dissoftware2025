import customtkinter as ctk
from tkinter import ttk
from models.database import SessionLocal

class PromocionesTab(ctk.CTkFrame):
    def __init__(self, parent, promociones_service):
        super().__init__(parent)
        self.promociones_service = promociones_service

        self.label = ctk.CTkLabel(self, text="Lista de Promociones", font=("Arial", 20))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Tipo", "Membresía"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Membresía", text="Membresía")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.reload_button = ctk.CTkButton(self, text="Cargar Promociones", command=self.cargar_datos)
        self.reload_button.pack(pady=5)

        self.cargar_datos()

    def cargar_datos(self):
        db = SessionLocal()
        try:
            promociones = self.promociones_service.listar_promociones(db)
            for item in self.tree.get_children():
                self.tree.delete(item)
            for promo in promociones:
                self.tree.insert("", "end", values=(
                    promo.id_promotions,
                    promo.Type,
                    "Sí" if promo.Membership else "No"
                ))
        finally:
            db.close()