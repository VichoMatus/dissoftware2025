import customtkinter as ctk
from tkinter import ttk
from models.database import SessionLocal

class FuncionesTab(ctk.CTkFrame):
    def __init__(self, parent, funcion_service):
        super().__init__(parent)
        self.funcion_service = funcion_service

        self.label = ctk.CTkLabel(self, text="Lista de Funciones", font=("Arial", 20))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Película", "Empleado", "Horario"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Película", text="Película")
        self.tree.heading("Empleado", text="Empleado")
        self.tree.heading("Horario", text="Horario")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.reload_button = ctk.CTkButton(self, text="Cargar Funciones", command=self.cargar_datos)
        self.reload_button.pack(pady=5)

        self.cargar_datos()

    def cargar_datos(self):
        db = SessionLocal()
        try:
            funciones = self.funcion_service.listar_funciones(db)
            for item in self.tree.get_children():
                self.tree.delete(item)
            for funcion in funciones:
                self.tree.insert("", "end", values=(
                    funcion.id_funcion,
                    funcion.id_pelicula,
                    funcion.employee_id,
                    str(funcion.Schedule)
                ))
        finally:
            db.close()
