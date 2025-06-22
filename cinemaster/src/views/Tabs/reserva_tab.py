import customtkinter as ctk
from tkinter import ttk
from models.database import SessionLocal

class ReservasTab(ctk.CTkFrame):
    def __init__(self, parent, reserva_service):
        super().__init__(parent)
        self.reserva_service = reserva_service

        self.label = ctk.CTkLabel(self, text="Lista de Reservas", font=("Arial", 20))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Cliente", "Función", "Promoción", "Empleado"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Función", text="Función")
        self.tree.heading("Promoción", text="Promoción")
        self.tree.heading("Empleado", text="Empleado")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.reload_button = ctk.CTkButton(self, text="Cargar Reservas", command=self.cargar_datos)
        self.reload_button.pack(pady=5)

        self.cargar_datos()

    def cargar_datos(self):
        db = SessionLocal()
        try:
            reservas = self.reserva_service.listar_reservas(db)
            for item in self.tree.get_children():
                self.tree.delete(item)
            for reserva in reservas:
                self.tree.insert("", "end", values=(
                    reserva.reservation_id,
                    reserva.client_id,
                    reserva.id_funcion,
                    reserva.id_promotions,
                    reserva.employee_id
                ))
        finally:
            db.close()