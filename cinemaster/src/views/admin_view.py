import customtkinter as ctk
from PIL import Image
from tkinter import ttk, messagebox
from datetime import datetime
from models.employee import Empleado
from models.database import SessionLocal


class AdminView(ctk.CTk):  # Asegúrate de que esta clase sea AdminView para manejar a los empleados
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Empleados")
        self.geometry("1280x720")
        self.vistas = {}


        self.crear_ui()

    def crear_ui(self):
        self.frame_header = ctk.CTkFrame(self)
        self.frame_header.pack(fill="x",padx=20, pady=10)

        try:
            logo_img = ctk.CTkImage(light_image=Image.open("src/views/images/logo.png"), size=(100, 100))
            logo_label = ctk.CTkLabel(self.frame_header, image=logo_img, text="")
        except:
            logo_label = ctk.CTkLabel(self.frame_header, text="[Logo]")

        logo_label.pack(side="left", padx=10)
        ctk.CTkLabel(self.frame_header, text="Gestión Administrador", font=("Arial", 24, "bold")).pack(side="left", padx=10)

        self.frame_menu = ctk.CTkFrame(self, width=150)
        self.frame_menu.pack(side="left", fill="y")

        botones = [
            ("Gestor Empleados", lambda: self.mostrar_vista("leer"))
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
        self.mostrar_Empleados()
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
        # CREAR (Formulario de agregar empleado)
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["crear"] = frame
        ctk.CTkLabel(frame, text="Agregar Empleado", font=("Arial", 16, "bold")).pack(pady=10)

        # FUNCIONES
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["Funciones"] = frame
        ctk.CTkLabel(frame, text="Funciones", font=("Arial", 16, "bold")).pack(pady=10)

        # Formulario oculto de crear empleado
        self.form_crear_frame = ctk.CTkFrame(frame)
        self.entry_crear_nombre = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Nombre")
        self.entry_crear_email = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Email")
        self.entry_crear_password = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Password", show="*")
        self.entry_crear_nombre.pack(pady=5)
        self.entry_crear_email.pack(pady=5)
        self.entry_crear_password.pack(pady=5)    
        self.form_crear_frame.pack_forget()  # Ocultamos el formulario inicialmente

        # LEER (Listado de empleados)
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["leer"] = frame
        ctk.CTkLabel(frame, text="Listado de Empleados", font=("Arial", 16, "bold")).pack(pady=10)

        # Treeview
        columns = ("ID", "Nombre", "Email")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(padx=10, pady=5, fill="x")

        # Botones de acción
        action_frame = ctk.CTkFrame(frame)
        action_frame.pack(pady=10)

        ctk.CTkButton(action_frame, text="Agregar Empleado",
              command=self.mostrar_formulario_creacion).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Actualizar Datos",
                  command=self.mostrar_formulario_actualizacion).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Eliminar Seleccionado", fg_color="red", hover_color="#b71c1c",
                  command=self.eliminar_empleado_seleccionado).pack(side="left", padx=10)

        # Formulario de creación oculto
        self.form_crear_frame = ctk.CTkFrame(frame)
        self.entry_crear_nombre_leer = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Nombre")
        self.entry_crear_email_leer = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Email")
        self.entry_crear_password_leer = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Contraseña")
        self.entry_crear_nombre_leer.pack(pady=5)
        self.entry_crear_email_leer.pack(pady=5)
        self.entry_crear_password_leer.pack(pady=5)
        ctk.CTkButton(self.form_crear_frame, text="Guardar Empleado", command=self.crear_empleado_desde_form).pack(pady=10)
        self.form_crear_frame.pack_forget()

    
        # ACTUALIZAR
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["actualizar"] = frame
        ctk.CTkLabel(frame, text="Actualizar Empleado", font=("Arial", 16, "bold")).pack(pady=10)
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
        ctk.CTkLabel(frame, text="Eliminar Empleado", font=("Arial", 16, "bold")).pack(pady=10)
        self.entry_eliminar_id = ctk.CTkEntry(frame, placeholder_text="ID")
        self.entry_eliminar_id.pack(pady=5)
        ctk.CTkButton(frame, text="Eliminar", command=self.eliminar_empleado_seleccionado).pack(pady=10)


    def mostrar_formulario_creacion(self):
        self.form_crear_frame.pack(pady=10)


    def crear_empleado_desde_form(self):
        nombre = self.entry_crear_nombre_leer.get()
        email = self.entry_crear_email_leer.get()
        password = self.entry_crear_password_leer.get()
        if not (nombre and email):
            self.agregar_a_historial("Todos los campos deben estar completos para crear un empleado.")
            return
        db = SessionLocal()
        try:
            nuevo = Empleado(Name=nombre, Email=email, Password=password)
            db.add(nuevo)
            db.commit()
            self.agregar_a_historial(f"Empleado '{nombre}' creado correctamente.")
            self.mostrar_Empleados()
            self.form_crear_frame.pack_forget()
        except Exception as e:
            self.agregar_a_historial(f"Error al crear empleado: {e}")
        finally:
            db.close()
    



    def mostrar_Empleados(self):
        if hasattr(self, "tree"):
            for item in self.tree.get_children():
                self.tree.delete(item)
        db = SessionLocal()
        try:
            empleados = db.query(Empleado).all()
            for emp in empleados:
                self.tree.insert("", "end", values=(emp.employee_id, emp.Name, emp.Email,emp.Password))
            self.agregar_a_historial("Listado de empleados actualizado.")
        except Exception as e:
            self.agregar_a_historial(f"Error al mostrar empleados: {e}")
        finally:
            db.close()



    def mostrar_formulario_actualizacion(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            self.agregar_a_historial("No hay empleado seleccionado.")
            return
        valores = self.tree.item(seleccionado)["values"]
        self.empleado_id_actual = valores[0]
    
        # Rellenar los campos existentes
        self.entry_actualizar_id.delete(0, "end")
        self.entry_actualizar_nombre.delete(0, "end")
        self.entry_actualizar_email.delete(0, "end")
        self.entry_actualizar_password.delete(0, "end")
    
        self.entry_actualizar_id.insert(0, valores[0])
        self.entry_actualizar_nombre.insert(0, valores[1])
        self.entry_actualizar_email.insert(0, valores[2])
        self

        self.mostrar_vista("actualizar")    



    def guardar_cambios_actualizacion(self):
        nuevo_nombre = self.entry_actualizar_nombre.get()
        nuevo_email = self.entry_actualizar_email.get()
        nuevo_password = self.entry_actualizar_password.get()
        empleado_id = self.entry_actualizar_id.get()

        if not (nuevo_nombre and nuevo_email):
            self.agregar_a_historial("Todos los campos deben estar completos.")
            return

        db = SessionLocal()
        try:
            # Verificar si el nuevo email ya existe en otro empleado
            email_duplicado = db.query(Empleado).filter(
                Empleado.Email == nuevo_email,
                Empleado.employee_id != empleado_id  # asegurarse de que no sea el mismo empleado
            ).first()

            if email_duplicado:
                self.agregar_a_historial(f"Ya existe un empleado con el email '{nuevo_email}'.")
                return

            empleado = db.query(Empleado).filter(Empleado.employee_id == empleado_id).first()
            if empleado:
                empleado.Name = nuevo_nombre
                empleado.Email = nuevo_email
                empleado.Password = nuevo_password
                db.commit()
                self.agregar_a_historial(f"Empleado ID {empleado_id} actualizado.")
                self.mostrar_Empleados()
            else:
                self.agregar_a_historial(f"No se encontró empleado con ID {empleado_id}.")
        except Exception as e:
            self.agregar_a_historial(f"Error al actualizar empleado: {e}")
        finally:
            db.close()



    def eliminar_empleado_seleccionado(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            self.agregar_a_historial("No hay empleado seleccionado.")
            return

        empleado_id = self.tree.item(seleccionado)["values"][0]
        
        # Mostrar un cuadro de confirmación antes de eliminar el empleado
        respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar el empleado con ID {empleado_id}?")
        if respuesta:
            db = SessionLocal()
            try:
                # Buscar al empleado por su ID
                empleado = db.query(Empleado).filter(Empleado.employee_id == empleado_id).first()
                if empleado:
                    db.delete(empleado)
                    db.commit()
                    self.agregar_a_historial(f"Empleado ID {empleado_id} eliminado.")
                    self.mostrar_Empleados()
                else:
                    self.agregar_a_historial(f"No se encontró empleado con ID {empleado_id}.")
            except Exception as e:
                self.agregar_a_historial(f"Error al eliminar empleado: {e}")
            finally:
                db.close()
        else:
            self.agregar_a_historial(f"Cancelada la eliminación del empleado ID {empleado_id}.")
