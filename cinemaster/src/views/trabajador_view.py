import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from datetime import datetime
from models.cliente import Cliente
from models.database import SessionLocal
import os


class ClienteView(ctk.CTk):
    def __init__(self, employee_name):
        super().__init__()
        self.title("Sistema de Gestión de Clientes")
        self.geometry("1280x720")

        self.vistas = {}
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.employee_name = employee_name
        self.crear_ui()

#
    def crear_ui(self):
        self.frame_header = ctk.CTkFrame(self, height=60)
        self.frame_header.pack(side="top", fill="x", padx=10, pady=10)

        try:
            current_dir = os.path.dirname(__file__)
            logo_path = os.path.join(current_dir, "images", "logo.png")
            self.logo_image = Image.open(logo_path)
            self.logo_image = self.logo_image.resize((100, 100))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            logo_label = ctk.CTkLabel(self.frame_header, image=self.logo_photo, text="")
        except Exception as e:
            logo_label = ctk.CTkLabel(self.frame_header, text="[Logo]")

        logo_label.pack(side="left", padx=10)
        ctk.CTkLabel(self.frame_header, text="Gestión Empleado", font=("Arial", 20, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(self.frame_header, text=f"Bienvenido, {self.employee_name.capitalize()}", font=("Arial", 20, "bold")).pack(side="right", padx=10)
#


        self.frame_menu = ctk.CTkFrame(self, width=150)
        self.frame_menu.pack(side="left", fill="y")
        botones = [
            ("Gestor Clientes", lambda: self.mostrar_vista("leer")),
            ("Funciones", lambda: self.mostrar_vista("Funciones")),
            ("Reservas", lambda: self.mostrar_vista("Reservas")),
            ("Promociones", lambda: self.mostrar_vista("Promociones")),
        ]
        for texto, accion in botones:
            ctk.CTkButton(self.frame_menu, text=texto, command=accion).pack(pady=10, padx=10, fill="x")

        self.frame_central = ctk.CTkFrame(self)
        self.frame_central.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.frame_vistas = ctk.CTkFrame(self.frame_central)
        self.frame_vistas.pack(side="top", fill="both", expand=True)

        self.frame_historial = ctk.CTkFrame(self.frame_central)
        self.frame_historial.pack(side="bottom", fill="x", padx=5)
        ctk.CTkLabel(self.frame_historial, text="Historial de acciones", font=("Arial", 14, "bold")).pack(pady=5)
        self.textbox_historial = ctk.CTkTextbox(self.frame_historial, height=100)
        self.textbox_historial.pack(padx=10, pady=5, fill="x")

        self.configurar_vistas()
        self.mostrar_clientes()
        self.mostrar_vista("leer")
        self.agregar_a_historial("¡Bienvenido! Gracias por preferirnos")

    def agregar_a_historial(self, mensaje):
        hora = datetime.now().strftime("%H:%M:%S")
        self.textbox_historial.insert("end", f"[{hora}] {mensaje}\n")
        self.textbox_historial.see("end")

    def mostrar_vista(self, vista):
        for frame in self.vistas.values():
            frame.pack_forget()
        self.vistas[vista].pack(fill="both", expand=True)

    def configurar_vistas(self):
        # CREAR (Formulario de agregar cliente)
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["crear"] = frame
        ctk.CTkLabel(frame, text="Agregar Cliente", font=("Arial", 16, "bold")).pack(pady=10)

        # FUNCIONES

#
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["Funciones"] = frame
        ctk.CTkLabel(frame, text="Funciones", font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(frame, text="🚧 La sección de Funciones está en construcción 🚧", font=("Arial", 20, "italic")).pack(pady=50)
        ctk.CTkButton(frame, text="ola")


        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["Reservas"] = frame
        ctk.CTkLabel(frame, text="Reservas", font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(frame, text="🚧 La sección de Reservas está en construcción 🚧", font=("Arial", 20, "italic")).pack(pady=50)


        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["Promociones"] = frame
        ctk.CTkLabel(frame, text="Promociones", font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(frame, text="🚧 La sección de Promociones está en construcción 🚧", font=("Arial", 20, "italic")).pack(pady=50)
#

        # Formulario oculto de crear cliente
        self.form_crear_frame = ctk.CTkFrame(frame)
        self.entry_crear_nombre = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Nombre")
        self.entry_crear_email = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Email")
        self.entry_crear_password = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Contraseña", show="*")
        self.entry_crear_nombre.pack(pady=5)
        self.entry_crear_email.pack(pady=5)
        self.entry_crear_password.pack(pady=5)    
        self.form_crear_frame.pack_forget()  # Ocultamos el formulario inicialmente

        # LEER (Listado de clientes)
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["leer"] = frame
        ctk.CTkLabel(frame, text="Listado de Clientes", font=("Arial", 16, "bold")).pack(pady=10)

        # Treeview
        columns = ("ID", "Nombre", "Email", "Membresía")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(padx=10, pady=5, fill="x")

        # Botones de acción
        action_frame = ctk.CTkFrame(frame)
        action_frame.pack(pady=10)

        ctk.CTkButton(action_frame, text="Agregar Cliente",
              command=self.mostrar_formulario_creacion).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Actualizar Datos",
                  command=self.mostrar_formulario_actualizacion).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Eliminar Seleccionado", fg_color="red", hover_color="#b71c1c",
                  command=self.eliminar_cliente_seleccionado).pack(side="left", padx=10)

        # Formulario de creación oculto
        self.form_crear_frame = ctk.CTkFrame(frame)
        self.entry_crear_nombre_leer = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Nombre")
        self.entry_crear_email_leer = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Email")
        self.entry_crear_password_leer = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Contraseña")
        self.entry_crear_nombre_leer.pack(pady=5)
        self.entry_crear_email_leer.pack(pady=5)
        self.entry_crear_password_leer.pack(pady=5)
        #self.entry_crear_membresia_leer.pack(pady=5)
        ctk.CTkButton(self.form_crear_frame, text="Guardar Cliente", command=self.crear_cliente_desde_form).pack(pady=10)
        self.form_crear_frame.pack_forget()

    
        # ACTUALIZAR
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["actualizar"] = frame
        ctk.CTkLabel(frame, text="Actualizar Cliente", font=("Arial", 16, "bold")).pack(pady=10)
        self.entry_actualizar_id = ctk.CTkEntry(frame, placeholder_text="ID")
        self.entry_actualizar_id.pack(pady=5)
        self.entry_actualizar_nombre = ctk.CTkEntry(frame, placeholder_text="Nuevo Nombre")
        self.entry_actualizar_nombre.pack(pady=5)
        self.entry_actualizar_email = ctk.CTkEntry(frame, placeholder_text="Nuevo Email")
        self.entry_actualizar_email.pack(pady=5)
        self.entry_actualizar_password = ctk.CTkEntry(frame, placeholder_text="Nueva Contraseña")
        self.entry_actualizar_password.pack(pady=5)
        ctk.CTkButton(frame, text="Actualizar", command=self.guardar_cambios_actualizacion).pack(pady=10)

        # ELIMINAR
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["eliminar"] = frame
        ctk.CTkLabel(frame, text="Eliminar Cliente", font=("Arial", 16, "bold")).pack(pady=10)
        self.entry_eliminar_id = ctk.CTkEntry(frame, placeholder_text="ID")
        self.entry_eliminar_id.pack(pady=5)
        ctk.CTkButton(frame, text="Eliminar", command=self.eliminar_cliente_seleccionado).pack(pady=10)


    def mostrar_formulario_creacion(self):
        self.form_crear_frame.pack(pady=10)


    def crear_cliente_desde_form(self):
        nombre = self.entry_crear_nombre_leer.get()
        email = self.entry_crear_email_leer.get()
        password = self.entry_crear_password_leer.get()
        if not (nombre and email):
            self.agregar_a_historial("Todos los campos deben estar completos para crear un cliente.")
            return
        db = SessionLocal()
        try:
            nuevo = Cliente(nombre=nombre, Email=email, Password=password, Reservation_history="", Membership=False)
            db.add(nuevo)
            db.commit()
            self.agregar_a_historial(f"Cliente '{nombre}' creado correctamente.")
            self.mostrar_clientes()
            self.form_crear_frame.pack_forget()
        except Exception as e:
            self.agregar_a_historial(f"Error al crear cliente: {e}")
        finally:
            db.close()
    



    def mostrar_clientes(self):
        if hasattr(self, "tree"):
            for item in self.tree.get_children():
                self.tree.delete(item)
        db = SessionLocal()
        try:
            clientes = db.query(Cliente).all()
            for cl in clientes:
                self.tree.insert("", "end", values=(cl.cliente_id, cl.nombre, cl.Email, "Sí" if cl.Membership else "No"))
            self.agregar_a_historial("Listado de clientes actualizado.")
        except Exception as e:
            self.agregar_a_historial(f"Error al mostrar clientes: {e}")
        finally:
            db.close()



    def mostrar_formulario_actualizacion(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            self.agregar_a_historial("No hay cliente seleccionado.")
            return
        valores = self.tree.item(seleccionado)["values"]
        self.cliente_id_actual = valores[0]
    
        # Rellenar los campos existentes
        self.entry_actualizar_id.delete(0, "end")
        self.entry_actualizar_nombre.delete(0, "end")
        self.entry_actualizar_email.delete(0, "end")
        self.entry_actualizar_password.delete(0, "end")
    
        self.entry_actualizar_id.insert(0, valores[0])
        self.entry_actualizar_nombre.insert(0, valores[1])
        self.entry_actualizar_email.insert(0, valores[2])

        self.mostrar_vista("actualizar")    



    def guardar_cambios_actualizacion(self):
        nuevo_nombre = self.entry_actualizar_nombre.get()
        nuevo_email = self.entry_actualizar_email.get()
        nuevo_password = self.entry_actualizar_password.get()
        cliente_id = self.entry_actualizar_id.get()

        if not (nuevo_nombre and nuevo_email):
            self.agregar_a_historial("Todos los campos deben estar completos.")
            return

        db = SessionLocal()
        try:
            # Verificar si el nuevo email ya existe en otro cliente
            email_duplicado = db.query(Cliente).filter(
                Cliente.Email == nuevo_email,
                Cliente.cliente_id != cliente_id  # asegurarse de que no sea el mismo cliente
            ).first()

            if email_duplicado:
                self.agregar_a_historial(f"Ya existe un cliente con el email '{nuevo_email}'.")
                return

            cliente = db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()
            if cliente:
                cliente.nombre = nuevo_nombre
                cliente.Email = nuevo_email
                cliente.Password = nuevo_password
                db.commit()
                self.agregar_a_historial(f"Cliente ID {cliente_id} actualizado.")
                self.mostrar_clientes()
            else:
                self.agregar_a_historial(f"No se encontró cliente con ID {cliente_id}.")
        except Exception as e:
            self.agregar_a_historial(f"Error al actualizar cliente: {e}")
        finally:
            db.close()



    def eliminar_cliente_seleccionado(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            self.agregar_a_historial("No hay cliente seleccionado.")
            return
        cliente_id = self.tree.item(seleccionado)["values"][0]
        db = SessionLocal()
        try:
            cliente = db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()
            if cliente:
                db.delete(cliente)
                db.commit()
                self.agregar_a_historial(f"Cliente ID {cliente_id} eliminado.")
                self.mostrar_clientes()
                messagebox.showwarning("Aviso", f"Usuario {cliente_id} Eliminado") #Mensaje al eliminar un usuario, se fe horrible de feo
            else:
                self.agregar_a_historial(f"No se encontró cliente con ID {cliente_id}.")
        except Exception as e:
            self.agregar_a_historial(f"Error al eliminar cliente: {e}")
        finally:
            db.close()
