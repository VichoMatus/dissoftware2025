import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

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

        self.cargar_datos()

    def cargar_datos(self):
        try:
            funciones = self.funcion_service.listar_funciones()
            for item in self.tree.get_children():
                self.tree.delete(item)
            for funcion in funciones:
                self.tree.insert("", "end", values=(
                    funcion["id_funcion"],
                    funcion["id_pelicula"],
                    funcion["employee_id"],
                    funcion["Schedule"]
                ))
        except Exception as e:
            print(f"Error al cargar funciones: {e}")

    def mostrar_formulario_agregar(self):
        top = ctk.CTkToplevel(self)
        top.title("Agregar Función")
        top.geometry("1100x700")

        lbl_pelicula = ctk.CTkLabel(top, text="ID Película:")
        lbl_pelicula.pack(pady=5)
        entry_pelicula = ctk.CTkEntry(top)
        entry_pelicula.pack(pady=5)

        lbl_empleado = ctk.CTkLabel(top, text="ID Empleado:")
        lbl_empleado.pack(pady=5)
        entry_empleado = ctk.CTkEntry(top)
        entry_empleado.pack(pady=5)

        lbl_fecha = ctk.CTkLabel(top, text="Fecha:")
        lbl_fecha.pack(pady=5)
        date_entry = DateEntry(top, date_pattern='yyyy-mm-dd')
        date_entry.pack(pady=5)

        lbl_hora = ctk.CTkLabel(top, text="Hora (HH:MM):")
        lbl_hora.pack(pady=5)
        hora_var = ctk.StringVar()
        hora_combo = ttk.Combobox(top, textvariable=hora_var, values=[
            f"{h:02d}:{m:02d}" for h in range(0,24) for m in (0,30)
        ])
        hora_combo.pack(pady=5)

        def guardar_funcion():
            id_pelicula = entry_pelicula.get()
            employee_id = entry_empleado.get()
            fecha = date_entry.get()
            hora = hora_var.get()
            if not id_pelicula or not employee_id or not fecha or not hora:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            try:
                schedule = f"{fecha}T{hora}:00"
                self.funcion_service.crear_funcion(int(id_pelicula), int(employee_id), schedule)
                messagebox.showinfo("Éxito", "Función agregada correctamente")
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la función:\n{e}")

        btn_guardar = ctk.CTkButton(top, text="Guardar", command=guardar_funcion, fg_color="#43a047")
        btn_guardar.pack(pady=15)

    def mostrar_formulario_actualizar(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Selecciona una función para actualizar")
            return

        valores = self.tree.item(selected, "values")
        if not valores:
            messagebox.showerror("Error", "No se pudo obtener la información de la función")
            return

        top = ctk.CTkToplevel(self)
        top.title("Actualizar Función")
        top.geometry("1100x700")

        lbl_pelicula = ctk.CTkLabel(top, text="ID Película:")
        lbl_pelicula.pack(pady=5)
        entry_pelicula = ctk.CTkEntry(top)
        entry_pelicula.insert(0, valores[1])
        entry_pelicula.pack(pady=5)

        lbl_empleado = ctk.CTkLabel(top, text="ID Empleado:")
        lbl_empleado.pack(pady=5)
        entry_empleado = ctk.CTkEntry(top)
        entry_empleado.insert(0, valores[2])
        entry_empleado.pack(pady=5)

        lbl_fecha = ctk.CTkLabel(top, text="Fecha:")
        lbl_fecha.pack(pady=5)
        date_entry = DateEntry(top, date_pattern='yyyy-mm-dd')
        # Extrae la fecha de Schedule
        fecha_val = valores[3][:10] if valores[3] else ""
        date_entry.set_date(fecha_val)
        date_entry.pack(pady=5)

        lbl_hora = ctk.CTkLabel(top, text="Hora (HH:MM):")
        lbl_hora.pack(pady=5)
        hora_var = ctk.StringVar()
        hora_val = valores[3][11:16] if valores[3] else ""
        hora_combo = ttk.Combobox(top, textvariable=hora_var, values=[
            f"{h:02d}:{m:02d}" for h in range(0,24) for m in (0,30)
        ])
        hora_combo.set(hora_val)
        hora_combo.pack(pady=5)

        def actualizar_funcion():
            id_pelicula = entry_pelicula.get()
            employee_id = entry_empleado.get()
            fecha = date_entry.get()
            hora = hora_var.get()
            if not id_pelicula or not employee_id or not fecha or not hora:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            try:
                schedule = f"{fecha}T{hora}:00"
                self.funcion_service.actualizar_funcion(
                    int(valores[0]), int(id_pelicula), int(employee_id), schedule
                )
                messagebox.showinfo("Éxito", "Función actualizada correctamente")
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la función:\n{e}")

        btn_actualizar = ctk.CTkButton(top, text="Actualizar", command=actualizar_funcion, fg_color="#fbc02d")
        btn_actualizar.pack(pady=15)

    def eliminar_funcion_seleccionada(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Selecciona una función para eliminar")
            return

        valores = self.tree.item(selected, "values")
        if not valores:
            messagebox.showerror("Error", "No se pudo obtener la información de la función")
            return

        confirm = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar la función con ID '{valores[0]}'?")
        if not confirm:
            return

        try:
            self.funcion_service.eliminar_funcion(int(valores[0]))
            messagebox.showinfo("Éxito", "Función eliminada correctamente")
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la función:\n{e}")