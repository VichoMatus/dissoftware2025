import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class FuncionesTab(ctk.CTkFrame):
    def __init__(self, parent, funcion_service, employee_id=None):
        super().__init__(parent)
        self.funcion_service = funcion_service
        self.employee_id = employee_id  # ID del empleado logueado
        self.peliculas_disponibles = []  # Cache de películas

        self.label = ctk.CTkLabel(self, text="Lista de Funciones", font=("Arial", 20))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Película", "Empleado", "Horario"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Película", text="Película")
        self.tree.heading("Empleado", text="Empleado")
        self.tree.heading("Horario", text="Horario")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Cargar películas disponibles al inicio
        self.cargar_peliculas_disponibles()
        self.cargar_datos()

    def cargar_datos(self):
        try:
            funciones = self.funcion_service.listar_funciones()
            for item in self.tree.get_children():
                self.tree.delete(item)
            for funcion in funciones:
                # Usar los nuevos campos de la API refactorizada
                pelicula_titulo = funcion.get("pelicula_titulo", f"ID: {funcion.get('id_pelicula')}")
                empleado_nombre = funcion.get("empleado_nombre", f"ID: {funcion.get('employee_id')}")
                
                self.tree.insert("", "end", values=(
                    funcion.get("id_funcion"),
                    pelicula_titulo,
                    empleado_nombre,
                    funcion.get("Schedule")
                ))
        except Exception as e:
            print(f"Error al cargar funciones: {e}")
            messagebox.showerror("Error", f"Error al cargar funciones:\n{e}")

    def cargar_peliculas_disponibles(self):
        """Carga la lista de películas disponibles desde la API"""
        try:
            self.peliculas_disponibles = self.funcion_service.obtener_peliculas_disponibles()
        except Exception as e:
            print(f"Error al cargar películas disponibles: {e}")
            self.peliculas_disponibles = []

    def mostrar_formulario_agregar(self):
        top = ctk.CTkToplevel(self)
        top.title("Agregar Función")
        top.geometry("500x600")

        # Dropdown para películas
        lbl_pelicula = ctk.CTkLabel(top, text="Película:", font=("Arial", 12, "bold"))
        lbl_pelicula.pack(pady=(20, 5))
        
        pelicula_var = ctk.StringVar()
        pelicula_values = [f"{p['Title']}" for p in self.peliculas_disponibles]
        pelicula_combo = ctk.CTkComboBox(
            top, 
            variable=pelicula_var,
            values=pelicula_values,
            width=300,
            height=35
        )
        pelicula_combo.pack(pady=5)

        # Campo de empleado (solo lectura, pre-rellenado)
        lbl_empleado = ctk.CTkLabel(top, text="Empleado (Auto):", font=("Arial", 12, "bold"))
        lbl_empleado.pack(pady=(15, 5))
        
        empleado_display = ctk.CTkEntry(top, width=300, height=35)
        empleado_display.insert(0, f"ID: {self.employee_id} (Usuario actual)")
        empleado_display.configure(state="disabled")  # Solo lectura
        empleado_display.pack(pady=5)

        # Fecha
        lbl_fecha = ctk.CTkLabel(top, text="Fecha:", font=("Arial", 12, "bold"))
        lbl_fecha.pack(pady=(15, 5))
        date_entry = DateEntry(top, date_pattern='yyyy-mm-dd', width=25)
        date_entry.pack(pady=5)

        # Hora
        lbl_hora = ctk.CTkLabel(top, text="Hora (HH:MM):", font=("Arial", 12, "bold"))
        lbl_hora.pack(pady=(15, 5))
        hora_var = ctk.StringVar()
        hora_combo = ctk.CTkComboBox(
            top,
            variable=hora_var,
            values=[f"{h:02d}:{m:02d}" for h in range(8, 24) for m in (0, 30)],
            width=300,
            height=35
        )
        hora_combo.pack(pady=5)

        def obtener_id_pelicula_seleccionada():
            """Obtiene el ID de la película seleccionada"""
            titulo_seleccionado = pelicula_var.get()
            for pelicula in self.peliculas_disponibles:
                if pelicula['Title'] == titulo_seleccionado:
                    return pelicula['id_pelicula']
            return None

        def guardar_funcion():
            titulo_pelicula = pelicula_var.get()
            fecha = date_entry.get()
            hora = hora_var.get()
            
            if not titulo_pelicula or not fecha or not hora:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            if not self.employee_id:
                messagebox.showerror("Error", "No se pudo obtener el ID del empleado")
                return
            
            id_pelicula = obtener_id_pelicula_seleccionada()
            if not id_pelicula:
                messagebox.showerror("Error", "Por favor seleccione una película válida")
                return
            
            try:
                schedule = f"{fecha}T{hora}:00"
                resultado = self.funcion_service.crear_funcion(id_pelicula, self.employee_id, schedule)
                messagebox.showinfo("Éxito", 
                    f"Función creada exitosamente!\n"
                    f"ID: {resultado.get('id_funcion', 'N/A')}\n"
                    f"Se crearon asientos A1-E8 automáticamente")
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la función:\n{e}")

        # Botones
        btn_frame = ctk.CTkFrame(top)
        btn_frame.pack(pady=30)
        
        btn_guardar = ctk.CTkButton(
            btn_frame, 
            text="Crear Función", 
            command=guardar_funcion, 
            fg_color="#43a047",
            width=120,
            height=40
        )
        btn_guardar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=top.destroy,
            fg_color="#f44336",
            width=120,
            height=40
        )
        btn_cancelar.pack(side="left", padx=10)

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
        top.geometry("500x600")

        # Dropdown para películas
        lbl_pelicula = ctk.CTkLabel(top, text="Película:", font=("Arial", 12, "bold"))
        lbl_pelicula.pack(pady=(20, 5))
        
        pelicula_var = ctk.StringVar()
        pelicula_values = [f"{p['Title']}" for p in self.peliculas_disponibles]
        pelicula_combo = ctk.CTkComboBox(
            top, 
            variable=pelicula_var,
            values=pelicula_values,
            width=300,
            height=35
        )
        
        # Pre-seleccionar la película actual (buscar por ID)
        current_pelicula_id = valores[1]  # ID película actual
        for pelicula in self.peliculas_disponibles:
            if str(pelicula['id_pelicula']) == str(current_pelicula_id):
                pelicula_combo.set(pelicula['Title'])
                break
        
        pelicula_combo.pack(pady=5)

        # Campo de empleado (solo lectura, pre-rellenado)
        lbl_empleado = ctk.CTkLabel(top, text="Empleado (Auto):", font=("Arial", 12, "bold"))
        lbl_empleado.pack(pady=(15, 5))
        
        empleado_display = ctk.CTkEntry(top, width=300, height=35)
        empleado_display.insert(0, f"ID: {self.employee_id} (Usuario actual)")
        empleado_display.configure(state="disabled")  # Solo lectura
        empleado_display.pack(pady=5)

        # Fecha
        lbl_fecha = ctk.CTkLabel(top, text="Fecha:", font=("Arial", 12, "bold"))
        lbl_fecha.pack(pady=(15, 5))
        date_entry = DateEntry(top, date_pattern='yyyy-mm-dd', width=25)
        # Extrae la fecha de Schedule
        fecha_val = valores[3][:10] if valores[3] else ""
        if fecha_val:
            date_entry.set_date(fecha_val)
        date_entry.pack(pady=5)

        # Hora
        lbl_hora = ctk.CTkLabel(top, text="Hora (HH:MM):", font=("Arial", 12, "bold"))
        lbl_hora.pack(pady=(15, 5))
        hora_var = ctk.StringVar()
        hora_val = valores[3][11:16] if valores[3] else ""
        hora_combo = ctk.CTkComboBox(
            top,
            variable=hora_var,
            values=[f"{h:02d}:{m:02d}" for h in range(8, 24) for m in (0, 30)],
            width=300,
            height=35
        )
        if hora_val:
            hora_combo.set(hora_val)
        hora_combo.pack(pady=5)

        def obtener_id_pelicula_seleccionada():
            """Obtiene el ID de la película seleccionada"""
            titulo_seleccionado = pelicula_var.get()
            for pelicula in self.peliculas_disponibles:
                if pelicula['Title'] == titulo_seleccionado:
                    return pelicula['id_pelicula']
            return None

        def actualizar_funcion():
            titulo_pelicula = pelicula_var.get()
            fecha = date_entry.get()
            hora = hora_var.get()
            
            if not titulo_pelicula or not fecha or not hora:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            if not self.employee_id:
                messagebox.showerror("Error", "No se pudo obtener el ID del empleado")
                return
            
            id_pelicula = obtener_id_pelicula_seleccionada()
            if not id_pelicula:
                messagebox.showerror("Error", "Por favor seleccione una película válida")
                return
            
            try:
                schedule = f"{fecha}T{hora}:00"
                self.funcion_service.actualizar_funcion(
                    int(valores[0]), id_pelicula, self.employee_id, schedule
                )
                messagebox.showinfo("Éxito", "Función actualizada correctamente")
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la función:\n{e}")

        # Botones
        btn_frame = ctk.CTkFrame(top)
        btn_frame.pack(pady=30)
        
        btn_actualizar = ctk.CTkButton(
            btn_frame, 
            text="Actualizar", 
            command=actualizar_funcion, 
            fg_color="#fbc02d",
            width=120,
            height=40
        )
        btn_actualizar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=top.destroy,
            fg_color="#f44336",
            width=120,
            height=40
        )
        btn_cancelar.pack(side="left", padx=10)

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