import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from datetime import datetime
from services.empleado_service import IEmpleadoCRUD
from services.cliente_service import IClienteCRUD
import os

class AdminView(ctk.CTk):
    def __init__(self, empleado_service: IEmpleadoCRUD, cliente_service: IClienteCRUD):
        super().__init__()
        self.empleado_service = empleado_service
        self.cliente_service = cliente_service
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
        nombre = self.entry_empleado_nombre.get()
        email = self.entry_empleado_email.get()
        password = self.entry_empleado_password.get()
        if not (nombre and email):
            self.agregar_a_historial("Complete todos los campos.")
            return
        try:
            self.empleado_service.agregar_empleado(nombre, email, password)
            self.agregar_a_historial(f"Empleado '{nombre}' agregado.")
            self.mostrar_empleados()
            self.form_empleado_frame.pack_forget()
        except Exception as e:
            self.agregar_a_historial(f"Error al crear empleado: {e}")

    def mostrar_empleados(self):
        for i in self.tree_empleados.get_children():
            self.tree_empleados.delete(i)
        try:
            for emp in self.empleado_service.listar_empleados():
                self.tree_empleados.insert("", "end", values=(emp.employee_id, emp.Name, emp.Email))
            self.agregar_a_historial("Listado de empleados actualizado.")
        except Exception as e:
            self.agregar_a_historial(f"Error al cargar empleados: {e}")

    def form_actualizar_empleado(self):
        item = self.tree_empleados.focus()
        if not item:
            self.agregar_a_historial("Selecciona un empleado.")
            return
        emp_id, nombre, email = self.tree_empleados.item(item)["values"]
        self.entry_empleado_nombre.delete(0, "end")
        self.entry_empleado_email.delete(0, "end")
        self.entry_empleado_password.delete(0, "end")
        self.entry_empleado_nombre.insert(0, nombre)
        self.entry_empleado_email.insert(0, email)

        if hasattr(self, 'boton_guardar_empleado'):
            self.boton_guardar_empleado.pack_forget()
        if hasattr(self, 'boton_actualizar_empleado'):
            self.boton_actualizar_empleado.destroy()

        def actualizar():
            try:
                self.empleado_service.actualizar_empleado(
                    emp_id,
                    self.entry_empleado_nombre.get(),
                    self.entry_empleado_email.get(),
                    self.entry_empleado_password.get()
                )
                self.agregar_a_historial(f"Empleado ID {emp_id} actualizado.")
                self.mostrar_empleados()
                self.form_empleado_frame.pack_forget()
            except Exception as e:
                self.agregar_a_historial(f"Error al actualizar: {e}")

        self.boton_actualizar_empleado = ctk.CTkButton(self.form_empleado_frame, text="Actualizar", command=actualizar)
        self.boton_actualizar_empleado.pack(pady=5)
        self.form_empleado_frame.pack(pady=10)

    def eliminar_empleado(self):
        item = self.tree_empleados.focus()
        if not item:
            self.agregar_a_historial("Selecciona un empleado.")
            return
        emp_id = self.tree_empleados.item(item)["values"][0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar empleado ID {emp_id}?"):
            try:
                self.empleado_service.eliminar_empleado(emp_id)
                self.agregar_a_historial(f"Empleado ID {emp_id} eliminado.")
                self.mostrar_empleados()
            except Exception as e:
                self.agregar_a_historial(f"Error al eliminar: {e}")

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
        nombre = self.entry_cliente_nombre.get()
        email = self.entry_cliente_email.get()
        password = self.entry_cliente_password.get()
        membresia = False  # Puedes cambiar esto según tu lógica/UI
        if not (nombre and email):
            self.agregar_a_historial("Complete todos los campos.")
            return
        try:
            self.cliente_service.agregar_cliente(nombre, email, password, membresia)
            self.agregar_a_historial(f"Cliente '{nombre}' agregado.")
            self.mostrar_clientes()
            self.form_cliente_frame.pack_forget()
        except Exception as e:
            self.agregar_a_historial(f"Error al crear cliente: {e}")

    def mostrar_clientes(self):
        for i in self.tree_clientes.get_children():
            self.tree_clientes.delete(i)
        try:
            for cl in self.cliente_service.listar_clientes():
                self.tree_clientes.insert("", "end", values=(cl.cliente_id, cl.nombre, cl.Email, "Sí" if cl.Membership else "No"))
            self.agregar_a_historial("Listado de clientes actualizado.")
        except Exception as e:
            self.agregar_a_historial(f"Error al cargar clientes: {e}")

    def form_actualizar_cliente(self):
        item = self.tree_clientes.focus()
        if not item:
            self.agregar_a_historial("Selecciona un cliente.")
            return
        cl_id, nombre, email, _ = self.tree_clientes.item(item)["values"]
        self.entry_cliente_nombre.delete(0, "end")
        self.entry_cliente_email.delete(0, "end")
        self.entry_cliente_password.delete(0, "end")
        self.entry_cliente_nombre.insert(0, nombre)
        self.entry_cliente_email.insert(0, email)

        if hasattr(self, 'boton_guardar_cliente'):
            self.boton_guardar_cliente.pack_forget()
        if hasattr(self, 'boton_actualizar_cliente'):
            self.boton_actualizar_cliente.destroy()

        def actualizar():
            try:
                self.cliente_service.actualizar_cliente(
                    cl_id,
                    self.entry_cliente_nombre.get(),
                    self.entry_cliente_email.get(),
                    self.entry_cliente_password.get(),
                    False  # O lo que corresponda
                )
                self.agregar_a_historial(f"Cliente ID {cl_id} actualizado.")
                self.mostrar_clientes()
                self.form_cliente_frame.pack_forget()
            except Exception as e:
                self.agregar_a_historial(f"Error al actualizar: {e}")

        self.boton_actualizar_cliente = ctk.CTkButton(self.form_cliente_frame, text="Actualizar", command=actualizar)
        self.boton_actualizar_cliente.pack(pady=5)
        self.form_cliente_frame.pack(pady=10)

    def eliminar_cliente(self):
        item = self.tree_clientes.focus()
        if not item:
            self.agregar_a_historial("Selecciona un cliente.")
            return
        cl_id = self.tree_clientes.item(item)["values"][0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar cliente ID {cl_id}?"):
            try:
                self.cliente_service.eliminar_cliente(cl_id)
                self.agregar_a_historial(f"Cliente ID {cl_id} eliminado.")
                self.mostrar_clientes()
            except Exception as e:
                self.agregar_a_historial(f"Error al eliminar: {e}")

    def clonar_cliente_seleccionado(self):
        item = self.tree_clientes.focus()
        if not item:
            self.agregar_a_historial("No hay cliente seleccionado para clonar.")
            return
        cl_id = self.tree_clientes.item(item)["values"][0]
        try:
            cliente_original = next((cl for cl in self.cliente_service.listar_clientes() if cl.cliente_id == cl_id), None)
            if cliente_original and hasattr(cliente_original, "clone"):
                cliente_clonado = cliente_original.clone()
                self.form_cliente()
                self.entry_cliente_nombre.delete(0, "end")
                self.entry_cliente_nombre.insert(0, cliente_clonado.nombre)
                self.entry_cliente_email.delete(0, "end")
                self.entry_cliente_email.insert(0, "")
                self.entry_cliente_password.delete(0, "end")
                self.entry_cliente_password.insert(0, "")
                self.agregar_a_historial(f"Cliente ID {cl_id} clonado. Edite los datos y guarde.")
            else:
                self.agregar_a_historial(f"No se encontró cliente con ID {cl_id} o no se puede clonar.")
        except Exception as e:
            self.agregar_a_historial(f"Error al clonar cliente: {e}")
