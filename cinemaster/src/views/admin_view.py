import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import requests  # [NUEVO] Para hacer peticiones a la API
import json      # [NUEVO] Para manejar errores de la API

# [NUEVO] Constante para la URL base de la API
API_BASE_URL = "http://127.0.0.1:8000"

class AdminView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Empleados y Clientes")
        self.geometry("1280x720")
        self.vistas = {}
        self.crear_ui()

    def crear_ui(self):
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill='x', padx=20, pady=10)

        current_dir = os.path.dirname(__file__)
        logo_path = os.path.join(current_dir, "images", "logo.png")

        self.logo_image = Image.open(logo_path)
        self.logo_image = self.logo_image.resize((100, 100))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = ctk.CTkLabel(self.header_frame, image=self.logo_photo, text="")
        self.logo_label.pack(side="left", padx=10)

        self.app_name_label = ctk.CTkLabel(self.header_frame, text="CineMaster", font=("Arial", 24, "bold"))
        self.app_name_label.pack(side="left", padx=10)

        self.frame_menu = ctk.CTkFrame(self, width=150)
        self.frame_menu.pack(side="left", fill="y")

        botones = [
            ("Gestor Empleados", lambda: self.mostrar_vista("empleados")),
            ("Gestor Clientes", lambda: self.mostrar_vista("clientes"))
        ]
        for texto, accion in botones:
            ctk.CTkButton(self.frame_menu, text=texto, command=accion).pack(pady=10, padx=10)

        self.frame_central = ctk.CTkFrame(self)
        self.frame_central.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.frame_vistas = ctk.CTkFrame(self.frame_central)
        self.frame_vistas.pack(side="top", fill="both", expand=True)

        self.frame_historial = ctk.CTkFrame(self.frame_central)
        self.frame_historial.pack(side="bottom", fill="x", padx=5)
        ctk.CTkLabel(self.frame_historial, text="Historial de acciones", font=("Arial", 14, "bold")).pack(pady=5)
        self.textbox_historial = ctk.CTkTextbox(self.frame_historial, height=100)
        self.textbox_historial.pack(padx=10, pady=5, fill="x")

        self.configurar_vistas_empleados()
        self.configurar_vistas_clientes()

        self.mostrar_vista("empleados")
        self.agregar_a_historial("¡Bienvenido! Gracias por preferirnos")

    def agregar_a_historial(self, mensaje):
        hora = datetime.now().strftime("%H:%M:%S")
        self.textbox_historial.insert("end", f"[{hora}] {mensaje}\n")
        self.textbox_historial.see("end")

    def mostrar_vista(self, nombre):
        for frame in self.vistas.values():
            frame.pack_forget()
        self.vistas[nombre].pack(fill="both", expand=True)

    # ============================ EMPLEADOS ============================

    def configurar_vistas_empleados(self):
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["empleados"] = frame
        ctk.CTkLabel(frame, text="Gestión de Empleados", font=("Arial", 16, "bold")).pack(pady=10)

        self.tree_empleados = ttk.Treeview(frame, columns=("ID", "Nombre", "Email"), show="headings", height=8)
        for col in ("ID", "Nombre", "Email"):
            self.tree_empleados.heading(col, text=col)
            self.tree_empleados.column(col, width=150)
        self.tree_empleados.pack(padx=10, pady=5, fill="x")

        action_frame = ctk.CTkFrame(frame)
        action_frame.pack(pady=10)
        ctk.CTkButton(action_frame, text="Agregar Empleado", command=self.form_empleado).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Actualizar Empleado", command=self.form_actualizar_empleado).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Eliminar Empleado", fg_color="red", hover_color="#b71c1c", command=self.eliminar_empleado).pack(side="left", padx=10)

        self.form_empleado_frame = ctk.CTkFrame(frame)
        self.entry_empleado_nombre = ctk.CTkEntry(self.form_empleado_frame, placeholder_text="Nombre")
        self.entry_empleado_email = ctk.CTkEntry(self.form_empleado_frame, placeholder_text="Email")
        self.entry_empleado_password = ctk.CTkEntry(self.form_empleado_frame, placeholder_text="Contraseña", show="*")
        for e in (self.entry_empleado_nombre, self.entry_empleado_email, self.entry_empleado_password):
            e.pack(pady=5)
        self.boton_guardar_empleado = ctk.CTkButton(self.form_empleado_frame, text="Guardar", command=self.guardar_empleado)
        self.boton_guardar_empleado.pack(pady=5)
        self.form_empleado_frame.pack_forget()

        self.mostrar_empleados()

    def form_empleado(self):
        self.entry_empleado_nombre.delete(0, "end")
        self.entry_empleado_email.delete(0, "end")
        self.entry_empleado_password.delete(0, "end")
        self.form_empleado_frame.pack(pady=10)
        self.boton_guardar_empleado.pack(pady=5)
        if hasattr(self, 'boton_actualizar_empleado'):
            self.boton_actualizar_empleado.pack_forget()

    def guardar_empleado(self):
        data = {
            "Name": self.entry_empleado_nombre.get(),
            "Email": self.entry_empleado_email.get(),
            "Password": self.entry_empleado_password.get()
        }
        if not (data["Name"] and data["Email"] and data["Password"]):
            self.agregar_a_historial("Error: Todos los campos son requeridos.")
            return

        try:
            response = requests.post(f"{API_BASE_URL}/admin/employees/", json=data)
            if response.status_code == 201:
                self.agregar_a_historial(f"Empleado '{data['Name']}' agregado con éxito.")
                self.mostrar_empleados()
                self.form_empleado_frame.pack_forget()
            else:
                self.agregar_a_historial(f"Error al crear empleado: {response.json().get('detail', response.text)}")
        except requests.exceptions.RequestException as e:
            self.agregar_a_historial(f"Error de conexión con la API: {e}")

    def mostrar_empleados(self):
        for i in self.tree_empleados.get_children():
            self.tree_empleados.delete(i)
        try:
            response = requests.get(f"{API_BASE_URL}/admin/employees/")
            if response.ok:
                for emp in response.json():
                    self.tree_empleados.insert("", "end", values=(emp["employee_id"], emp["Name"], emp["Email"]))
                self.agregar_a_historial("Listado de empleados actualizado.")
            else:
                self.agregar_a_historial("Error al cargar empleados desde la API.")
        except requests.exceptions.RequestException as e:
            self.agregar_a_historial(f"Error de conexión con la API: {e}")

    def form_actualizar_empleado(self):
        item = self.tree_empleados.focus()
        if not item:
            self.agregar_a_historial("Selecciona un empleado para actualizar.")
            return
        emp_id, nombre, email = self.tree_empleados.item(item)["values"]
        self.entry_empleado_nombre.delete(0, "end"); self.entry_empleado_nombre.insert(0, nombre)
        self.entry_empleado_email.delete(0, "end"); self.entry_empleado_email.insert(0, email)
        self.entry_empleado_password.delete(0, "end")
        self.entry_empleado_password.configure(placeholder_text="Nueva contraseña (opcional)")

        if hasattr(self, 'boton_guardar_empleado'): self.boton_guardar_empleado.pack_forget()
        if hasattr(self, 'boton_actualizar_empleado'): self.boton_actualizar_empleado.destroy()

        def actualizar():
            data = {
                "Name": self.entry_empleado_nombre.get(),
                "Email": self.entry_empleado_email.get()
            }
            password = self.entry_empleado_password.get()
            if password: data["Password"] = password

            try:
                response = requests.put(f"{API_BASE_URL}/admin/employees/{emp_id}", json=data)
                if response.ok:
                    self.agregar_a_historial(f"Empleado ID {emp_id} actualizado.")
                    self.mostrar_empleados()
                    self.form_empleado_frame.pack_forget()
                else:
                    self.agregar_a_historial(f"Error al actualizar: {response.json().get('detail', response.text)}")
            except requests.exceptions.RequestException as e:
                self.agregar_a_historial(f"Error de conexión con la API: {e}")

        self.boton_actualizar_empleado = ctk.CTkButton(self.form_empleado_frame, text="Actualizar", command=actualizar)
        self.boton_actualizar_empleado.pack(pady=5)
        self.form_empleado_frame.pack(pady=10)

    def eliminar_empleado(self):
        item = self.tree_empleados.focus()
        if not item:
            self.agregar_a_historial("Selecciona un empleado para eliminar.")
            return
        emp_id = self.tree_empleados.item(item)["values"][0]
        if messagebox.askyesno("Confirmar", f"¿Realmente desea eliminar al empleado ID {emp_id}?"):
            try:
                response = requests.delete(f"{API_BASE_URL}/admin/employees/{emp_id}")
                if response.status_code == 204:
                    self.agregar_a_historial(f"Empleado ID {emp_id} eliminado.")
                    self.mostrar_empleados()
                else:
                    self.agregar_a_historial(f"Error al eliminar: {response.json().get('detail', response.text)}")
            except requests.exceptions.RequestException as e:
                self.agregar_a_historial(f"Error de conexión con la API: {e}")

    # ============================ CLIENTES ============================

    def configurar_vistas_clientes(self):
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["clientes"] = frame
        ctk.CTkLabel(frame, text="Gestión de Clientes", font=("Arial", 16, "bold")).pack(pady=10)

        self.tree_clientes = ttk.Treeview(frame, columns=("ID", "Nombre", "Email", "Membresía"), show="headings", height=8)
        for col in ("ID", "Nombre", "Email", "Membresía"):
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, width=150)
        self.tree_clientes.pack(padx=10, pady=5, fill="x")

        action_frame = ctk.CTkFrame(frame)
        action_frame.pack(pady=10)
        ctk.CTkButton(action_frame, text="Agregar Cliente", command=self.form_cliente).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Actualizar Cliente", command=self.form_actualizar_cliente).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Eliminar Cliente", fg_color="red", hover_color="#b71c1c", command=self.eliminar_cliente).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Clonar Cliente", command=self.clonar_cliente_seleccionado).pack(side="left", padx=10)

        self.form_cliente_frame = ctk.CTkFrame(frame)
        self.entry_cliente_nombre = ctk.CTkEntry(self.form_cliente_frame, placeholder_text="Nombre")
        self.entry_cliente_email = ctk.CTkEntry(self.form_cliente_frame, placeholder_text="Email")
        self.entry_cliente_password = ctk.CTkEntry(self.form_cliente_frame, placeholder_text="Contraseña", show="*")
        for e in (self.entry_cliente_nombre, self.entry_cliente_email, self.entry_cliente_password):
            e.pack(pady=5)
        self.boton_guardar_cliente = ctk.CTkButton(self.form_cliente_frame, text="Guardar", command=self.guardar_cliente)
        self.boton_guardar_cliente.pack(pady=5)        
        self.form_cliente_frame.pack_forget()

        self.mostrar_clientes()

    def form_cliente(self):
        self.entry_cliente_nombre.delete(0, "end")
        self.entry_cliente_email.delete(0, "end")
        self.entry_cliente_password.delete(0, "end")
        self.form_cliente_frame.pack(pady=10)
        self.boton_guardar_cliente.pack(pady=5)
        if hasattr(self, 'boton_actualizar_cliente'):
            self.boton_actualizar_cliente.pack_forget()

    def guardar_cliente(self):
        data = {
            "nombre": self.entry_cliente_nombre.get(),
            "Email": self.entry_cliente_email.get(),
            "Password": self.entry_cliente_password.get()
        }
        if not (data["nombre"] and data["Email"] and data["Password"]):
            self.agregar_a_historial("Error: Todos los campos son requeridos.")
            return

        try:
            response = requests.post(f"{API_BASE_URL}/admin/clients/", json=data)
            if response.status_code == 201:
                self.agregar_a_historial(f"Cliente '{data['nombre']}' agregado con éxito.")
                self.mostrar_clientes()
                self.form_cliente_frame.pack_forget()
            else:
                self.agregar_a_historial(f"Error al crear cliente: {response.json().get('detail', response.text)}")
        except requests.exceptions.RequestException as e:
            self.agregar_a_historial(f"Error de conexión con la API: {e}")

    def mostrar_clientes(self):
        for i in self.tree_clientes.get_children():
            self.tree_clientes.delete(i)
        try:
            response = requests.get(f"{API_BASE_URL}/admin/clients/")
            if response.ok:
                for cl in response.json():
                    self.tree_clientes.insert("", "end", values=(cl["cliente_id"], cl["nombre"], cl["Email"], "Sí" if cl["Membership"] else "No"))
                self.agregar_a_historial("Listado de clientes actualizado.")
            else:
                self.agregar_a_historial("Error al cargar clientes desde la API.")
        except requests.exceptions.RequestException as e:
            self.agregar_a_historial(f"Error de conexión con la API: {e}")

    def form_actualizar_cliente(self):
        item = self.tree_clientes.focus()
        if not item:
            self.agregar_a_historial("Selecciona un cliente para actualizar.")
            return
        cl_id, nombre, email, _ = self.tree_clientes.item(item)["values"]
        self.entry_cliente_nombre.delete(0, "end"); self.entry_cliente_nombre.insert(0, nombre)
        self.entry_cliente_email.delete(0, "end"); self.entry_cliente_email.insert(0, email)
        self.entry_cliente_password.delete(0, "end")
        self.entry_cliente_password.configure(placeholder_text="Nueva contraseña (opcional)")

        if hasattr(self, 'boton_guardar_cliente'): self.boton_guardar_cliente.pack_forget()
        if hasattr(self, 'boton_actualizar_cliente'): self.boton_actualizar_cliente.destroy()

        def actualizar():
            data = {"nombre": self.entry_cliente_nombre.get(), "Email": self.entry_cliente_email.get()}
            password = self.entry_cliente_password.get()
            if password: data["Password"] = password
            
            try:
                response = requests.put(f"{API_BASE_URL}/admin/clients/{cl_id}", json=data)
                if response.ok:
                    self.agregar_a_historial(f"Cliente ID {cl_id} actualizado.")
                    self.mostrar_clientes()
                    self.form_cliente_frame.pack_forget()
                else:
                    self.agregar_a_historial(f"Error al actualizar: {response.json().get('detail', response.text)}")
            except requests.exceptions.RequestException as e:
                self.agregar_a_historial(f"Error de conexión con la API: {e}")

        self.boton_actualizar_cliente = ctk.CTkButton(self.form_cliente_frame, text="Actualizar", command=actualizar)
        self.boton_actualizar_cliente.pack(pady=5)
        self.form_cliente_frame.pack(pady=10)

    def eliminar_cliente(self):
        item = self.tree_clientes.focus()
        if not item:
            self.agregar_a_historial("Selecciona un cliente para eliminar.")
            return
        cl_id = self.tree_clientes.item(item)["values"][0]
        if messagebox.askyesno("Confirmar", f"¿Realmente desea eliminar al cliente ID {cl_id}?"):
            try:
                response = requests.delete(f"{API_BASE_URL}/admin/clients/{cl_id}")
                if response.status_code == 204:
                    self.agregar_a_historial(f"Cliente ID {cl_id} eliminado.")
                    self.mostrar_clientes()
                else:
                    self.agregar_a_historial(f"Error al eliminar: {response.json().get('detail', response.text)}")
            except requests.exceptions.RequestException as e:
                self.agregar_a_historial(f"Error de conexión con la API: {e}")

    def clonar_cliente_seleccionado(self):
        item = self.tree_clientes.focus()
        if not item:
            self.agregar_a_historial("No hay cliente seleccionado para clonar.")
            return
        cliente_id = self.tree_clientes.item(item)["values"][0]
        try:
            response = requests.post(f"{API_BASE_URL}/admin/clients/clone/{cliente_id}")
            if response.ok:
                cloned_data = response.json()
                self.form_cliente()
                self.entry_cliente_nombre.insert(0, cloned_data.get('nombre', ''))
                self.entry_cliente_email.insert(0, '') # Dejar vacío para el nuevo clon
                self.entry_cliente_password.insert(0, '')
                self.agregar_a_historial(f"Datos del cliente ID {cliente_id} clonados. Rellene y guarde.")
            else:
                self.agregar_a_historial(f"Error al clonar: {response.json().get('detail', response.text)}")
        except requests.exceptions.RequestException as e:
            self.agregar_a_historial(f"Error de conexión con la API: {e}")
