import customtkinter as ctk
import shutil
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from models.cliente import Cliente
from models.database import Funcion, Reserva, Empleado, Pelicula, Asiento, HorarioAsientos, Horario
from models.database import SessionLocal
import os



def create_40_seats_for_showtime(db_session, horario_id):
    seat_ids = [f'{chr(65 + i)}{j+1}' for i in range(5) for j in range(8)]  # A1..E8

    for seat_id in seat_ids:
        existing_seat = db_session.query(Asiento).filter(Asiento.ids_seats == seat_id).first()
        if not existing_seat:
            new_seat = Asiento(ids_seats=seat_id)
            db_session.add(new_seat)
            db_session.commit()
        existing_relation = db_session.query(HorarioAsientos).filter(
            HorarioAsientos.horario_id == horario_id,
            HorarioAsientos.asiento_id == seat_id
        ).first()
        if not existing_relation:
            horario_asiento = HorarioAsientos(
                horario_id=horario_id,
                asiento_id=seat_id,
                Available=True
            )
            db_session.add(horario_asiento)
            db_session.commit()

#---------- CLASE PRINCIPAL ----------#
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

#---------- UI GENERAL ----------#
    def crear_ui(self):
        # Encabezado
        self.frame_header = ctk.CTkFrame(self, height=60)
        self.frame_header.pack(side="top", fill="x", padx=10, pady=10)

        try:
            current_dir = os.path.dirname(__file__)
            logo_path = os.path.join(current_dir, "images", "logo.png")
            logo_image = Image.open(logo_path).resize((100, 100))
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = ctk.CTkLabel(self.frame_header, image=self.logo_photo, text="")
        except Exception:
            logo_label = ctk.CTkLabel(self.frame_header, text="[Logo]")

        logo_label.pack(side="left", padx=10)
        ctk.CTkLabel(self.frame_header, text="Gestión Empleado", font=("Arial", 20, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(self.frame_header, text=f"Bienvenido, {self.employee_name.capitalize()}", font=("Arial", 20, "bold")).pack(side="right", padx=10)

        # Menú lateral
        self.frame_menu = ctk.CTkFrame(self, width=150)
        self.frame_menu.pack(side="left", fill="y")
        botones = [
            ("Gestor Clientes", lambda: self.mostrar_vista("leer")),
            ("Películas", lambda: self.mostrar_vista("Peliculas")),
            ("Funciones", lambda: self.mostrar_vista("Funciones")),
            ("Reservas", lambda: self.mostrar_vista("Reservas")),
            ("Promociones", lambda: self.mostrar_vista("Promociones")),
        ]
        for texto, accion in botones:
            ctk.CTkButton(self.frame_menu, text=texto, command=accion).pack(pady=10, padx=10, fill="x")

        # Zona central
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

#---------- HISTORIAL ----------#
    def agregar_a_historial(self, mensaje):
        hora = datetime.now().strftime("%H:%M:%S")
        self.textbox_historial.insert("end", f"[{hora}] {mensaje}\n")
        self.textbox_historial.see("end")

#---------- CONTROL DE VISTAS ----------#
    def mostrar_vista(self, vista):
        for frame in self.vistas.values():
            frame.pack_forget()
        self.vistas[vista].pack(fill="both", expand=True)

    def configurar_vistas(self):
        self.configurar_vista_leer()
        self.configurar_vista_actualizar()
        self.configurar_vista_eliminar()
        self.configurar_vista_peliculas()
        self.configurar_vista_funciones()
        self.configurar_vista_reservas()
        #self.configurar_vista_promociones()

#----------------------------------------.-.-.-_-_- Vista de Clientes-_-_.-.-.----------------------------------------#
    def configurar_vista_leer(self):
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["leer"] = frame

        ctk.CTkLabel(frame, text="Listado de Clientes", font=("Arial", 16, "bold")).pack(pady=10)

        columns = ("ID", "Nombre", "Email", "Membresía")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(padx=10, pady=5, fill="x")

        action_frame = ctk.CTkFrame(frame)
        action_frame.pack(pady=10)
        ctk.CTkButton(action_frame, text="Agregar Cliente", command=self.mostrar_formulario_creacion).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Actualizar Datos", command=self.mostrar_formulario_actualizacion).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Eliminar Seleccionado", fg_color="red", hover_color="#b71c1c", command=self.eliminar_cliente_seleccionado).pack(side="left", padx=10)

        self.form_crear_frame = ctk.CTkFrame(frame)
        self.entry_crear_nombre_leer = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Nombre")
        self.entry_crear_email_leer = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Email")
        self.entry_crear_password_leer = ctk.CTkEntry(self.form_crear_frame, placeholder_text="Contraseña")
        self.entry_crear_nombre_leer.pack(pady=5)
        self.entry_crear_email_leer.pack(pady=5)
        self.entry_crear_password_leer.pack(pady=5)
        ctk.CTkButton(self.form_crear_frame, text="Guardar Cliente", command=self.crear_cliente_desde_form).pack(pady=10)
        self.form_crear_frame.pack_forget()

    def configurar_vista_actualizar(self):
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["actualizar"] = frame
        ctk.CTkLabel(frame, text="Actualizar Cliente", font=("Arial", 16, "bold")).pack(pady=10)

        self.entry_actualizar_id = ctk.CTkEntry(frame, placeholder_text="ID")
        self.entry_actualizar_nombre = ctk.CTkEntry(frame, placeholder_text="Nuevo Nombre")
        self.entry_actualizar_email = ctk.CTkEntry(frame, placeholder_text="Nuevo Email")
        self.entry_actualizar_password = ctk.CTkEntry(frame, placeholder_text="Nueva Contraseña")

        self.entry_actualizar_id.pack(pady=5)
        self.entry_actualizar_nombre.pack(pady=5)
        self.entry_actualizar_email.pack(pady=5)
        self.entry_actualizar_password.pack(pady=5)
        ctk.CTkButton(frame, text="Actualizar", command=self.guardar_cambios_actualizacion).pack(pady=10)

    def configurar_vista_eliminar(self):
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["eliminar"] = frame
        ctk.CTkLabel(frame, text="Eliminar Cliente", font=("Arial", 16, "bold")).pack(pady=10)
        self.entry_eliminar_id = ctk.CTkEntry(frame, placeholder_text="ID")
        self.entry_eliminar_id.pack(pady=5)
        ctk.CTkButton(frame, text="Eliminar", command=self.eliminar_cliente_seleccionado).pack(pady=10)
#----------------------------------------.-.-.-_-_- Vista de Clientes-_-_.-.-.----------------------------------------#



    #------------------------------------.-.-.-_-_- Vista de Peliculaa-_-_.-.-.----------------------------------------#
    def configurar_vista_peliculas(self):
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["Peliculas"] = frame

        ctk.CTkLabel(frame, text="Gestión de Películas", font=("Arial", 18, "bold")).pack(pady=10)

        tabs = ctk.CTkTabview(frame)
        tabs.pack(expand=True, fill="both", padx=10, pady=10)
        tab_lista = tabs.add("Listado")
        tab_crear = tabs.add("Crear")

        # --- TAB LISTADO ---
        columnas = ("ID", "Título", "Duración", "Género", "Imagen")
        self.tree_peliculas = ttk.Treeview(tab_lista, columns=columnas, show="headings", height=12)
        for col in columnas:
            self.tree_peliculas.heading(col, text=col)
            self.tree_peliculas.column(col, width=150)
        self.tree_peliculas.pack(pady=10, padx=10, fill="x")

        btns_frame = ctk.CTkFrame(tab_lista)
        btns_frame.pack(pady=5)
        ctk.CTkButton(btns_frame, text="Actualizar Lista", command=self.cargar_peliculas).pack(side="left", padx=5)
        ctk.CTkButton(btns_frame, text="Eliminar Seleccionado", fg_color="red", hover_color="#b71c1c", command=self.eliminar_pelicula).pack(side="left", padx=5)

        # --- TAB CREAR ---
        form_frame = ctk.CTkFrame(tab_crear)
        form_frame.pack(pady=20, fill="both", expand=True)

        # Panel izquierdo: Previsualización de imagen
        self.preview_frame = ctk.CTkFrame(form_frame, width=250, height=300)
        self.preview_frame.pack(side="left", padx=10, pady=10)
        self.label_preview_imagen = ctk.CTkLabel(self.preview_frame, text="Sin imagen", width=250, height=300)
        self.label_preview_imagen.pack(padx=10, pady=10)

        # Panel derecho: formulario
        form_inputs = ctk.CTkFrame(form_frame)
        form_inputs.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        # Entrada: Título
        ctk.CTkLabel(form_inputs, text="Título:").pack(anchor="w", padx=10)
        self.entry_titulo = ctk.CTkEntry(form_inputs)
        self.entry_titulo.pack(padx=10, pady=5, fill="x")

        # Entrada: Duración
        ctk.CTkLabel(form_inputs, text="Duración (minutos):").pack(anchor="w", padx=10)
        self.entry_duracion = ctk.CTkEntry(form_inputs)
        self.entry_duracion.pack(padx=10, pady=5, fill="x")

        # Entrada: Género
        ctk.CTkLabel(form_inputs, text="Género:").pack(anchor="w", padx=10)
        self.entry_genero = ctk.CTkEntry(form_inputs)
        self.entry_genero.pack(padx=10, pady=5, fill="x")

        # Botón Buscar imagen
        self.btn_seleccionar_imagen = ctk.CTkButton(form_inputs, text="Buscar imagen", command=self.seleccionar_imagen_pelicula)
        self.btn_seleccionar_imagen.pack(padx=10, pady=10)

        # Botones Guardar y Cancelar en fila
        btns_row = ctk.CTkFrame(form_inputs)
        btns_row.pack(pady=10)

        self.btn_guardar_pelicula = ctk.CTkButton(btns_row, text="Guardar", command=self.crear_pelicula_desde_form)
        self.btn_guardar_pelicula.pack(side="right", padx=10)

        self.cargar_peliculas()
        self.agregar_a_historial("[INFO] Vista de películas cargada.")
#----------------------------------------.-.-.-_-_- Vista de Peliculaa-_-_.-.-.----------------------------------------#



#----------------------------------------.-.-.-_-_- Vista de Funciones-_-_.-.-.----------------------------------------#
    def configurar_vista_funciones(self):
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["Funciones"] = frame

        ctk.CTkLabel(frame, text="Listado de Funciones", font=("Arial", 16, "bold")).pack(pady=10)

        columnas = ("ID Función", "ID Película", "ID Empleado", "Horario")
        self.funcion_tree = ttk.Treeview(frame, columns=columnas, show="headings", selectmode="browse", height=8)
        for col in columnas:
            self.funcion_tree.heading(col, text=col)
            self.funcion_tree.column(col, width=150, anchor="center")
        self.funcion_tree.pack(padx=10, pady=5, fill="x")

        action_frame = ctk.CTkFrame(frame)
        action_frame.pack(pady=10)
        ctk.CTkButton(action_frame, text="Agregar Función", command=self.mostrar_formulario_creacion_funcion).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Actualizar Función", command=self.mostrar_formulario_actualizacion_funcion).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Eliminar Seleccionado", fg_color="red", hover_color="#b71c1c", command=self.eliminar_funcion).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Actualizar Lista", command=self.cargar_funciones).pack(side="left", padx=10)

        # ---------- FORMULARIO ----------
        self.form_funcion_frame = ctk.CTkFrame(frame)
        self.form_funcion_frame.pack_forget()

        ctk.CTkLabel(self.form_funcion_frame, text="Película:").pack(pady=2)
        self.menu_peliculas = ctk.CTkOptionMenu(self.form_funcion_frame, values=[])
        self.menu_peliculas.pack(pady=5)

        ctk.CTkLabel(self.form_funcion_frame, text="Empleado:").pack(pady=2)
        self.menu_empleados = ctk.CTkOptionMenu(self.form_funcion_frame, values=[])
        self.menu_empleados.pack(pady=5)

        ctk.CTkLabel(self.form_funcion_frame, text="Horario:").pack(pady=2)
        self.entry_horario = ctk.CTkEntry(self.form_funcion_frame, placeholder_text="Ej: 2025-06-01 20:00")
        self.entry_horario.pack(pady=5)

        self.btn_guardar_funcion = ctk.CTkButton(self.form_funcion_frame, text="Guardar Función", command=self.crear_funcion_desde_form)
        self.btn_guardar_funcion.pack(pady=10)

        # Cargar funciones al iniciar
        self.cargar_funciones()
        self.agregar_a_historial("[INFO] Vista de funciones cargada.")
#----------------------------------------.-.-.-_-_- Vista de Funciones-_-_.-.-.----------------------------------------#



#----------------------------------------.-.-.-_-_- Vista de Reservas-_-_.-.-.----------------------------------------#
    def configurar_vista_reservas(self):
        # Frame principal
        frame = ctk.CTkFrame(self.frame_vistas)
        self.vistas["Reservas"] = frame

        # Título
        ctk.CTkLabel(frame, text="Gestión de Reservas", font=("Arial", 18, "bold")).pack(pady=10)

        # Layout principal (izquierda: treeview, derecha: formulario)
        layout = ctk.CTkFrame(frame)
        layout.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Panel izquierdo (Treeview) ---
        left_panel = ctk.CTkFrame(layout)
        left_panel.pack(side="left", fill="both", expand=True, padx=5)

        columnas = ("ID Reserva", "ID Cliente", "ID Función", "ID Promoción", "ID Empleado")
        self.reserva_tree = ttk.Treeview(left_panel, columns=columnas, show="headings", selectmode="browse", height=12)

        for col in columnas:
            self.reserva_tree.heading(col, text=col)
            self.reserva_tree.column(col, width=140, anchor="center")
        self.reserva_tree.pack(padx=10, pady=5, fill="both", expand=True)

        # Botones de acción
        action_frame = ctk.CTkFrame(left_panel)
        action_frame.pack(pady=5)
        ctk.CTkButton(action_frame, text="Agregar", command=self.mostrar_formulario_creacion_reserva).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="Actualizar", command=self.mostrar_formulario_actualizacion_reserva).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="Eliminar", fg_color="red", hover_color="#b71c1c", command=self.eliminar_reserva).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="Recargar", command=self.cargar_reservas).pack(side="left", padx=5)

        # --- Panel derecho (Formulario) ---
        right_panel = ctk.CTkFrame(layout)
        right_panel.pack(side="right", fill="y", padx=5)

        self.form_reserva_frame = ctk.CTkFrame(right_panel, corner_radius=10)
        self.form_reserva_frame.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(self.form_reserva_frame, text="Formulario de Reserva", font=("Arial", 15, "bold")).pack(pady=10)

        # Cargar datos para menús desplegables
        with SessionLocal() as db:
            # Clientes
            self.clientes_dict = {cliente.Email: cliente.cliente_id for cliente in db.query(Cliente).all()}

            # Funciones (extraemos la película con consulta separada)
            self.funciones_dict = {}
            funciones = db.query(Funcion).all()
            for f in funciones:
                pelicula = db.query(Pelicula).filter(Pelicula.id_pelicula == f.id_pelicula).first()
                titulo = pelicula.Title if pelicula else "Sin título"
                key = f"{titulo}, id:{f.id_funcion}"
                self.funciones_dict[key] = f.id_funcion

            # Empleados
            self.empleados_dict = {empleado.Email: empleado.employee_id for empleado in db.query(Empleado).all()}

        # Selector Cliente
        ctk.CTkLabel(self.form_reserva_frame, text="Cliente:").pack(pady=(10, 2), anchor="w", padx=10)
        self.opcion_email_cliente = ctk.CTkOptionMenu(self.form_reserva_frame, values=list(self.clientes_dict.keys()))
        self.opcion_email_cliente.pack(pady=5, padx=10, fill="x")

        # Selector Función
        ctk.CTkLabel(self.form_reserva_frame, text="Función:").pack(pady=(10, 2), anchor="w", padx=10)
        self.opcion_funcion = ctk.CTkOptionMenu(self.form_reserva_frame, values=list(self.funciones_dict.keys()))
        self.opcion_funcion.pack(pady=5, padx=10, fill="x")

        # Campo ID Promoción
        ctk.CTkLabel(self.form_reserva_frame, text="ID Promoción:").pack(pady=(10, 2), anchor="w", padx=10)
        self.entry_id_promocion = ctk.CTkEntry(self.form_reserva_frame, placeholder_text="Ingrese ID promoción")
        self.entry_id_promocion.pack(pady=5, padx=10, fill="x")

        # Selector Empleado
        ctk.CTkLabel(self.form_reserva_frame, text="Empleado:").pack(pady=(10, 2), anchor="w", padx=10)
        self.opcion_email_empleado = ctk.CTkOptionMenu(self.form_reserva_frame, values=list(self.empleados_dict.keys()))
        self.opcion_email_empleado.pack(pady=5, padx=10, fill="x")

        # Botón Guardar
        self.btn_guardar_reserva = ctk.CTkButton(
            self.form_reserva_frame,
            text="Guardar Reserva",
            command=self.crear_reserva_desde_form
        )
        self.btn_guardar_reserva.pack(pady=20)

        # Ocultar formulario al inicio
        self.form_reserva_frame.pack_forget()

        # Cargar reservas en treeview (asegúrate de tener esta función definida)
        self.cargar_reservas()
        self.agregar_a_historial("[INFO] Vista de reservas cargada.")



#----------------------------------------.-.-.-_-_- Vista de Reservas-_-_.-.-.----------------------------------------#



#----------------------------------------.-.-.-_-_- Funciones de Clientes-_-_.-.-.----------------------------------------#
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
            email_duplicado = db.query(Cliente).filter(
                Cliente.Email == nuevo_email,
                Cliente.cliente_id != cliente_id
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
                messagebox.showwarning("Aviso", f"Usuario {cliente_id} Eliminado")
            else:
                self.agregar_a_historial(f"No se encontró cliente con ID {cliente_id}.")
        finally:
            db.close()
#----------------------------------------.-.-.-_-_- Funciones de Clientes-_-_.-.-.----------------------------------------#



#----------------------------------------.-.-.-_-_- Funciones de Peliculas-_-_.-.-.----------------------------------------#
    def cargar_peliculas(self):
        if hasattr(self, "tree_peliculas"):
            for item in self.tree_peliculas.get_children():
                self.tree_peliculas.delete(item)
            db = SessionLocal()
            try:
                peliculas = db.query(Pelicula).all()
                for p in peliculas:
                    self.tree_peliculas.insert("", "end", values=(p.id_pelicula, p.Title, p.Duration, p.Gender, p.Image_path))
                self.agregar_a_historial("Películas cargadas correctamente.")
            except Exception as e:
                self.agregar_a_historial(f"Error al cargar películas: {e}")
            finally:
                db.close()

    def seleccionar_imagen_pelicula(self):
        ruta_origen = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.gif")]
        )
        if ruta_origen:
            ruta_destino = self.guardar_imagen_en_carpeta_peliculas(ruta_origen)
            self.ruta_imagen_guardada = ruta_destino
            self.mostrar_imagen_previa(ruta_destino)

    def guardar_imagen_en_carpeta_peliculas(self, origen_path):
        ruta_carpeta = os.path.join(os.path.dirname(__file__), "images")
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
        nombre_archivo = os.path.basename(origen_path)
        destino_path = os.path.join(ruta_carpeta, nombre_archivo)
        shutil.copy(origen_path, destino_path)
        return destino_path

    def mostrar_imagen_previa(self, ruta_imagen):
        try:
            image = Image.open(ruta_imagen)
            image = image.resize((200, 300))
            photo = ImageTk.PhotoImage(image)

            self.label_preview_imagen.configure(image=photo, text="")
            self.label_preview_imagen.image = photo
        except Exception as e:
            self.agregar_a_historial(f"Error al mostrar imagen: {e}")

    def crear_pelicula_desde_form(self):
        titulo = self.entry_titulo.get()
        duracion = self.entry_duracion.get()
        genero = self.entry_genero.get()
        imagen = self.ruta_imagen_guardada

        if not (titulo and duracion and imagen):
            self.agregar_a_historial("Título, duración e imagen son obligatorios.")
            return

        db = SessionLocal()
        try:
            nueva = Pelicula(Title=titulo, Duration=int(duracion), Gender=genero, Image_path=imagen)
            db.add(nueva)
            db.commit()
            self.agregar_a_historial(f"Película '{titulo}' creada correctamente.")
            self.cargar_peliculas()
        except Exception as e:
            self.agregar_a_historial(f"Error al crear película: {e}")
        finally:
            db.close()

    def eliminar_pelicula(self):
        seleccionado = self.tree_peliculas.focus()
        if not seleccionado:
            self.agregar_a_historial("No hay película seleccionada.")
            return

        pelicula_id = self.tree_peliculas.item(seleccionado)["values"][0]
        db = SessionLocal()
        try:
            pelicula = db.query(Pelicula).filter(Pelicula.id_pelicula == pelicula_id).first()
            if pelicula:
                db.delete(pelicula)
                db.commit()
                self.agregar_a_historial(f"Película ID {pelicula_id} eliminada.")
                self.cargar_peliculas()
            else:
                self.agregar_a_historial("No se encontró la película.")
        finally:
            db.close()
#----------------------------------------.-.-.-_-_- Funciones de Peliculas-_-_.-.-.----------------------------------------#


#----------------------------------------.-.-.-_-_- Funciones de Funciones-_-_.-.-.----------------------------------------#
#-..................................#
    def crear_funcion_desde_form(self):
        # Obtener valores seleccionados desde los OptionMenus
        titulo_pelicula = self.menu_peliculas.get()
        nombre_empleado = self.menu_empleados.get()
        horario_str = self.entry_horario.get()

        # Validar que no estén vacíos
        if not all([titulo_pelicula, nombre_empleado, horario_str]):
            self.agregar_a_historial("Todos los campos deben estar completos para agregar una función.")
            return

        # Convertir string a datetime
        try:
            horario = datetime.strptime(horario_str, "%Y-%m-%d %H:%M")
        except ValueError:
            self.agregar_a_historial("[ERROR] Formato de fecha/hora inválido. Use 'YYYY-MM-DD HH:MM'.")
            return

        # Obtener los IDs correspondientes desde los diccionarios
        id_pelicula = self.dict_peliculas.get(titulo_pelicula)
        employee_id = self.dict_empleados.get(nombre_empleado)

        if id_pelicula is None or employee_id is None:
            self.agregar_a_historial("Error al obtener los IDs de película o empleado.")
            return

        db = SessionLocal()
        try:
            # Crear la función con horario
            nueva_funcion = Funcion(
                id_pelicula=id_pelicula,
                employee_id=employee_id,
                Schedule=horario
            )
            db.add(nueva_funcion)
            db.commit()
            db.refresh(nueva_funcion)

            # Crear el horario para esa función (registro en tabla Horario)
            nuevo_horario = Horario(
                fecha=horario,
                pelicula_id=id_pelicula
            )
            db.add(nuevo_horario)
            db.commit()
            db.refresh(nuevo_horario)

            # Crear 40 asientos para el horario recién creado
            create_40_seats_for_showtime(db, nuevo_horario.id)

            self.agregar_a_historial(f"Función creada correctamente para '{titulo_pelicula}' a las {horario_str}, con asientos generados.")
            self.cargar_funciones()
            self.form_funcion_frame.pack_forget()
        except Exception as e:
            self.agregar_a_historial(f"[ERROR] No se pudo crear la función: {str(e)}")
        finally:
            db.close()



    def mostrar_formulario_creacion_funcion(self):
        # Cargar listas desde DB
        db = SessionLocal()
        peliculas = db.query(Pelicula).all()
        empleados = db.query(Empleado).all()
        db.close()

        # Crear diccionarios
        self.dict_peliculas = {p.Title: p.id_pelicula for p in peliculas}
        self.dict_empleados = {e.Name: e.employee_id for e in empleados}

        # Establecer opciones en los menús
        self.menu_peliculas.configure(values=list(self.dict_peliculas.keys()))
        self.menu_empleados.configure(values=list(self.dict_empleados.keys()))

        if self.dict_peliculas:
            self.menu_peliculas.set(list(self.dict_peliculas.keys())[0])
        if self.dict_empleados:
            self.menu_empleados.set(list(self.dict_empleados.keys())[0])

        self.entry_horario.delete(0, "end")
        self.btn_guardar_funcion.configure(
            text="Guardar Función",
            command=self.crear_funcion_desde_form
        )
        self.form_funcion_frame.pack(pady=10)

    def mostrar_formulario_actualizacion_funcion(self):
        seleccionado = self.funcion_tree.focus()
        if not seleccionado:
            self.agregar_a_historial("No hay función seleccionada.")
            return

        valores = self.funcion_tree.item(seleccionado)["values"]
        self.funcion_id_actual = valores[0]

        # Cargar datos de películas y empleados nuevamente
        db = SessionLocal()
        peliculas = db.query(Pelicula).all()
        empleados = db.query(Empleado).all()
        db.close()

        self.dict_peliculas = {p.Title: p.id_pelicula for p in peliculas}
        self.dict_empleados = {e.Name: e.employee_id for e in empleados}

        # Establecer opciones
        self.menu_peliculas.configure(values=list(self.dict_peliculas.keys()))
        self.menu_empleados.configure(values=list(self.dict_empleados.keys()))

        # Buscar nombres asociados al ID actual
        id_pelicula_actual = valores[1]
        id_empleado_actual = valores[2]

        titulo_pelicula = next((t for t, i in self.dict_peliculas.items() if i == id_pelicula_actual), None)
        nombre_empleado = next((n for n, i in self.dict_empleados.items() if i == id_empleado_actual), None)

        self.menu_peliculas.set(titulo_pelicula if titulo_pelicula else list(self.dict_peliculas.keys())[0])
        self.menu_empleados.set(nombre_empleado if nombre_empleado else list(self.dict_empleados.keys())[0])

        self.entry_horario.delete(0, "end")
        self.entry_horario.insert(0, valores[3])

        self.btn_guardar_funcion.configure(
            text="Actualizar Función",
            command=self.actualizar_funcion
        )
        self.form_funcion_frame.pack(pady=10)

    def actualizar_funcion(self):
        if not hasattr(self, 'funcion_id_actual'):
            self.agregar_a_historial("No hay función seleccionada para actualizar")
            return

        titulo_pelicula = self.menu_peliculas.get()
        nombre_empleado = self.menu_empleados.get()
        nuevo_horario = self.entry_horario.get()

        id_pelicula = self.dict_peliculas.get(titulo_pelicula)
        id_empleado = self.dict_empleados.get(nombre_empleado)

        if not all([id_pelicula, id_empleado, nuevo_horario]):
            self.agregar_a_historial("Todos los campos son requeridos")
            return

        db = SessionLocal()
        try:
            funcion = db.query(Funcion).filter(Funcion.id_funcion == self.funcion_id_actual).first()
            if funcion:
                funcion.id_pelicula = id_pelicula
                funcion.employee_id = id_empleado
                funcion.Schedule = nuevo_horario
                db.commit()
                self.agregar_a_historial(f"Función ID {self.funcion_id_actual} actualizada correctamente")
                self.cargar_funciones()
                self.form_funcion_frame.pack_forget()
            else:
                self.agregar_a_historial("No se encontró la función para actualizar")
        except Exception as e:
            self.agregar_a_historial(f"Error al actualizar función: {str(e)}")
        finally:
            db.close()
#.................--------------------------------.............................#

    def eliminar_funcion(self):
        seleccionado = self.funcion_tree.focus()
        if not seleccionado:
            self.agregar_a_historial("No hay función seleccionada.")
            return

        funcion_id = self.funcion_tree.item(seleccionado)["values"][0]

        db = SessionLocal()
        try:
            funcion = db.query(Funcion).filter(Funcion.id_funcion == funcion_id).first()
            if funcion:
                db.delete(funcion)
                db.commit()
                self.agregar_a_historial(f"Función ID {funcion_id} eliminada.")
                self.cargar_funciones()
            else:
                self.agregar_a_historial("No se encontró la función.")
        finally:
            db.close()

    def cargar_funciones(self):
        for item in self.funcion_tree.get_children():
            self.funcion_tree.delete(item)

        db = SessionLocal()
        try:
            funciones = db.query(Funcion).all()
            for f in funciones:
                self.funcion_tree.insert("", "end", values=(
                    f.id_funcion, f.id_pelicula, f.employee_id, f.Schedule
                ))
            self.agregar_a_historial("Lista de funciones actualizada.")
        except Exception as e:
            self.agregar_a_historial(f"Error al cargar funciones: {e}")
        finally:
            db.close()
#----------------------------------------.-.-.-_-_- Funciones de Funciones-_-_.-.-.----------------------------------------#


#----------------------------------------.-.-.-_-_-Funciones de Reservas-_-_.-.-.----------------------------------------#
    def crear_reserva_desde_form(self):
        email_cliente = self.opcion_email_cliente.get()
        id_cliente = self.clientes_dict.get(email_cliente)

        funcion_texto = self.opcion_funcion.get()
        id_funcion = self.funciones_dict.get(funcion_texto)

        promocion_id_texto = self.entry_id_promocion.get()
        id_promocion = int(promocion_id_texto) if promocion_id_texto.isdigit() else None

        email_empleado = self.opcion_email_empleado.get()
        id_empleado = self.empleados_dict.get(email_empleado)

        # Validación básica
        if not all([id_cliente, id_funcion, id_empleado]):
            self.agregar_a_historial("Debe completar Cliente, Función y Empleado.")
            return

        db = SessionLocal()
        try:
            nueva_reserva = Reserva(
                client_id=id_cliente,
                id_funcion=id_funcion,
                id_promotions=id_promocion,
                employee_id=id_empleado
            )
            db.add(nueva_reserva)
            db.commit()

            self.agregar_a_historial("Reserva creada exitosamente.")
            self.cargar_reservas()
            self.form_reserva_frame.pack_forget()
        except Exception as e:
            self.agregar_a_historial(f"Error al crear reserva: {e}")
        finally:
            db.close()

    def mostrar_formulario_creacion_reserva(self):
        primeros_clientes = list(self.clientes_dict.keys())
        self.opcion_email_cliente.set(primeros_clientes[0] if primeros_clientes else "")

        primeras_funciones = list(self.funciones_dict.keys())
        self.opcion_funcion.set(primeras_funciones[0] if primeras_funciones else "")

        self.entry_id_promocion.delete(0, "end")

        primeros_empleados = list(self.empleados_dict.keys())
        self.opcion_email_empleado.set(primeros_empleados[0] if primeros_empleados else "")

        self.btn_guardar_reserva.configure(text="Guardar Reserva", command=self.crear_reserva_desde_form)
        self.form_reserva_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def mostrar_formulario_actualizacion_reserva(self):
        seleccionado = self.reserva_tree.focus()
        if not seleccionado:
            self.agregar_a_historial("No hay reserva seleccionada.")
            return

        valores = self.reserva_tree.item(seleccionado)["values"]
        self.reserva_id_actual = valores[0]

        with SessionLocal() as db:
            clientes = db.query(Cliente).all()
            self.clientes_dict = {c.Email: c.cliente_id for c in clientes}

            self.funciones_dict = {}
            funciones = db.query(Funcion).all()
            for f in funciones:
                key = f"Funcion{f.id_funcion}, id:{f.id_funcion}"
                self.funciones_dict[key] = f.id_funcion

            empleados = db.query(Empleado).all()
            self.empleados_dict = {e.Email: e.employee_id for e in empleados}

        email_actual_cliente = next(
            (email for email, cid in self.clientes_dict.items() if cid == valores[1]), 
            list(self.clientes_dict.keys())[0] if self.clientes_dict else ""
        )
        
        funcion_actual = next(
            (k for k, v in self.funciones_dict.items() if v == valores[2]), 
            list(self.funciones_dict.keys())[0] if self.funciones_dict else ""
        )
        
        email_actual_empleado = next(
            (email for email, eid in self.empleados_dict.items() if eid == valores[4]), 
            list(self.empleados_dict.keys())[0] if self.empleados_dict else ""
        )

        for widget in self.form_reserva_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.form_reserva_frame, text="Actualizar Reserva", font=("Arial", 15, "bold")).pack(pady=10)

        ctk.CTkLabel(self.form_reserva_frame, text="Cliente:").pack(pady=(10, 2), anchor="w", padx=10)
        self.opcion_email_cliente = ctk.CTkOptionMenu(
            self.form_reserva_frame, 
            values=list(self.clientes_dict.keys())
        )
        self.opcion_email_cliente.set(email_actual_cliente)
        self.opcion_email_cliente.pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(self.form_reserva_frame, text="Función:").pack(pady=(10, 2), anchor="w", padx=10)
        self.opcion_funcion = ctk.CTkOptionMenu(
            self.form_reserva_frame, 
            values=list(self.funciones_dict.keys())
        )
        self.opcion_funcion.set(funcion_actual)
        self.opcion_funcion.pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(self.form_reserva_frame, text="ID Promoción:").pack(pady=(10, 2), anchor="w", padx=10)
        self.entry_id_promocion = ctk.CTkEntry(
            self.form_reserva_frame, 
            placeholder_text="Ingrese ID promoción"
        )
        if valores[3] is not None:
            self.entry_id_promocion.insert(0, str(valores[3]))
        self.entry_id_promocion.pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(self.form_reserva_frame, text="Empleado:").pack(pady=(10, 2), anchor="w", padx=10)
        self.opcion_email_empleado = ctk.CTkOptionMenu(
            self.form_reserva_frame, 
            values=list(self.empleados_dict.keys())
        )
        self.opcion_email_empleado.set(email_actual_empleado)
        self.opcion_email_empleado.pack(pady=5, padx=10, fill="x")

        self.btn_guardar_reserva = ctk.CTkButton(
            self.form_reserva_frame,
            text="Actualizar Reserva",
            command=self.actualizar_reserva
        )
        self.btn_guardar_reserva.pack(pady=20)
        self.form_reserva_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def actualizar_reserva(self):
        if not hasattr(self, 'reserva_id_actual'):
            self.agregar_a_historial("No hay reserva seleccionada para actualizar")
            return
        
        email_seleccionado = self.opcion_email_cliente.get()
        nuevo_cliente = self.clientes_dict.get(email_seleccionado)

        funcion_seleccionada = self.opcion_funcion.get()
        nueva_funcion = self.funciones_dict.get(funcion_seleccionada)

        empleado_seleccionado = self.opcion_email_empleado.get()
        nuevo_empleado = self.empleados_dict.get(empleado_seleccionado)

        nueva_promocion = self.entry_id_promocion.get().strip()
        if nueva_promocion == "":
            nueva_promocion = None

        if not all([nuevo_cliente, nueva_funcion, nuevo_empleado]):
            self.agregar_a_historial("Cliente, función y empleado son campos requeridos")
            return

        db = SessionLocal()
        try:
            reserva = db.query(Reserva).filter(Reserva.reservation_id == self.reserva_id_actual).first()
            if reserva:
                reserva.client_id = nuevo_cliente
                reserva.id_funcion = nueva_funcion
                reserva.id_promotions = nueva_promocion
                reserva.employee_id = nuevo_empleado

                db.commit()
                self.agregar_a_historial(f"Reserva ID {self.reserva_id_actual} actualizada correctamente")
                self.cargar_reservas()
                self.form_reserva_frame.pack_forget()
            else:
                self.agregar_a_historial("No se encontró la reserva para actualizar")
        except Exception as e:
            self.agregar_a_historial(f"Error al actualizar reserva: {str(e)}")
        finally:
            db.close()

    def eliminar_reserva(self):
        seleccionado = self.reserva_tree.focus()
        if not seleccionado:
            self.agregar_a_historial("No hay reserva seleccionada.")
            return

        reserva_id = self.reserva_tree.item(seleccionado)["values"][0]

        db = SessionLocal()
        try:
            reserva = db.query(Reserva).filter(Reserva.reservation_id == reserva_id).first()
            if reserva:
                db.delete(reserva)
                db.commit()
                self.agregar_a_historial(f"Reserva ID {reserva_id} eliminada.")
                self.cargar_reservas()
            else:
                self.agregar_a_historial("No se encontró la reserva.")
        finally:
            db.close()

    def cargar_reservas(self):
        for item in self.reserva_tree.get_children():
            self.reserva_tree.delete(item)

        db = SessionLocal()
        try:
            reservas = db.query(Reserva).all()
            for r in reservas:
                self.reserva_tree.insert("", "end", values=(
                    r.reservation_id, r.client_id, r.id_funcion, r.id_promotions, r.employee_id
                ))
            self.agregar_a_historial("Lista de reservas actualizada.")
        except Exception as e:
            self.agregar_a_historial(f"Error al cargar reservas: {e}")
        finally:
            db.close()
#----------------------------------------.-.-.-_-_-Funciones de Reservas-_-_.-.-.----------------------------------------#