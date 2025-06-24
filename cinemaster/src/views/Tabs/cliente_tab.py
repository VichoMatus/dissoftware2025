import customtkinter as ctk
from tkinter import ttk
from models.database import SessionLocal

class ClientesTab(ctk.CTkFrame):
    def __init__(self, parent, cliente_service):
        super().__init__(parent)
        self.cliente_service = cliente_service

        self.label = ctk.CTkLabel(self, text="Lista de Clientes", font=("Arial", 20))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Correo", "Membresía"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Membresía", text="Membresía")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.reload_button = ctk.CTkButton(self, text="Cargar Clientes", command=self.cargar_datos)
        self.reload_button.pack(pady=5)

        self.cargar_datos()

    def cargar_datos(self):
        db = SessionLocal()
        try:
            clientes = self.cliente_service.listar_clientes(db)
            for item in self.tree.get_children():
                self.tree.delete(item)
            for cliente in clientes:
                self.tree.insert("", "end", values=(
                    cliente.cliente_id,
                    cliente.nombre,
                    cliente.Email,
                    "Sí" if cliente.Membership else "No"
                ))
        finally:
            db.close()