import customtkinter as ctk
from tkinter import ttk, messagebox

class ReservasTab(ctk.CTkFrame):
    def __init__(self, parent, reserva_service):
        super().__init__(parent)
        self.reserva_service = reserva_service

        self.label = ctk.CTkLabel(self, text="Lista de Reservas", font=("Arial", 20))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Cliente", "Función", "Empleado"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="ID Cliente")
        self.tree.heading("Función", text="ID Función")
        self.tree.heading("Empleado", text="ID Empleado")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_datos()

    def cargar_datos(self):
        try:
            reservas = self.reserva_service.listar_reservas()
            for item in self.tree.get_children():
                self.tree.delete(item)
            for reserva in reservas:
                self.tree.insert("", "end", values=(
                    reserva["reservation_id"],
                    reserva["client_id"],
                    reserva["id_funcion"],
                    reserva["employee_id"]
                ))
        except Exception as e:
            print(f"Error al cargar reservas: {e}")

    def mostrar_formulario_agregar(self):
        top = ctk.CTkToplevel(self)
        top.title("Agregar Reserva")
        top.geometry("350x300")

        lbl_cliente = ctk.CTkLabel(top, text="ID Cliente:")
        lbl_cliente.pack(pady=5)
        entry_cliente = ctk.CTkEntry(top)
        entry_cliente.pack(pady=5)

        lbl_funcion = ctk.CTkLabel(top, text="ID Función:")
        lbl_funcion.pack(pady=5)
        entry_funcion = ctk.CTkEntry(top)
        entry_funcion.pack(pady=5)

        lbl_empleado = ctk.CTkLabel(top, text="ID Empleado:")
        lbl_empleado.pack(pady=5)
        entry_empleado = ctk.CTkEntry(top)
        entry_empleado.pack(pady=5)

        def guardar_reserva():
            client_id = entry_cliente.get()
            id_funcion = entry_funcion.get()
            employee_id = entry_empleado.get()
            
            if not client_id or not id_funcion or not employee_id:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            try:
                self.reserva_service.crear_reserva(
                    client_id=int(client_id),
                    id_funcion=int(id_funcion),
                    employee_id=int(employee_id)
                )
                messagebox.showinfo("Éxito", "Reserva agregada correctamente")
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la reserva:\n{e}")

        btn_guardar = ctk.CTkButton(top, text="Guardar", command=guardar_reserva, fg_color="#43a047")
        btn_guardar.pack(pady=15)

    def mostrar_formulario_actualizar(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Selecciona una reserva para actualizar")
            return

        valores = self.tree.item(selected, "values")
        if not valores:
            messagebox.showerror("Error", "No se pudo obtener la información de la reserva")
            return

        top = ctk.CTkToplevel(self)
        top.title("Actualizar Reserva")
        top.geometry("350x300")

        lbl_cliente = ctk.CTkLabel(top, text="ID Cliente:")
        lbl_cliente.pack(pady=5)
        entry_cliente = ctk.CTkEntry(top)
        entry_cliente.insert(0, valores[1])
        entry_cliente.pack(pady=5)

        lbl_funcion = ctk.CTkLabel(top, text="ID Función:")
        lbl_funcion.pack(pady=5)
        entry_funcion = ctk.CTkEntry(top)
        entry_funcion.insert(0, valores[2])
        entry_funcion.pack(pady=5)

        lbl_empleado = ctk.CTkLabel(top, text="ID Empleado:")
        lbl_empleado.pack(pady=5)
        entry_empleado = ctk.CTkEntry(top)
        entry_empleado.insert(0, valores[3])
        entry_empleado.pack(pady=5)

        def actualizar_reserva():
            client_id = entry_cliente.get()
            id_funcion = entry_funcion.get()
            employee_id = entry_empleado.get()
            
            if not client_id or not id_funcion or not employee_id:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            try:
                self.reserva_service.actualizar_reserva(
                    reservation_id=int(valores[0]),
                    client_id=int(client_id),
                    id_funcion=int(id_funcion),
                    employee_id=int(employee_id)
                )
                messagebox.showinfo("Éxito", "Reserva actualizada correctamente")
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la reserva:\n{e}")

        btn_actualizar = ctk.CTkButton(top, text="Actualizar", command=actualizar_reserva, fg_color="#fbc02d")
        btn_actualizar.pack(pady=15)

    def eliminar_reserva_seleccionada(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Selecciona una reserva para eliminar")
            return

        valores = self.tree.item(selected, "values")
        if not valores:
            messagebox.showerror("Error", "No se pudo obtener la información de la reserva")
            return

        confirm = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar la reserva ID {valores[0]}?")
        if not confirm:
            return

        try:
            self.reserva_service.eliminar_reserva(int(valores[0]))
            messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la reserva:\n{e}")