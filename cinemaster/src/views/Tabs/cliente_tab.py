import customtkinter as ctk
from tkinter import ttk, messagebox

class ClientesTab(ctk.CTkFrame):
    def __init__(self, parent, cliente_service):
        super().__init__(parent)
        self.cliente_service = cliente_service

        ctk.CTkLabel(self, text="Listado de Clientes", font=("Arial", 16, "bold")).pack(pady=10)

        columns = ("ID", "Nombre", "Email", "Membresía")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(padx=10, pady=5, fill="x")

        action_frame = ctk.CTkFrame(self)
        action_frame.pack(pady=10)
        ctk.CTkButton(action_frame, text="Agregar Cliente").pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Actualizar Datos").pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Eliminar Seleccionado", fg_color="red", hover_color="#b71c1c").pack(side="left", padx=10)