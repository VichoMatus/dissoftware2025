import customtkinter as ctk
from tkinter import messagebox
from models.database import SessionLocal
from models.auth_controller import AuthController
from PIL import Image, ImageTk
from views.cartelera_view import MainView
import os

class LoginView(ctk.CTk):
    def __init__(self, open_register_view, open_cartelera_view, open_trabajador_view, open_admin_view):
        super().__init__()
        self.title("Login")
        self.geometry("1280x720")

        # Funciones para abrir la ventana de registro y la cartelera y la vista trabajador
        self.open_register_view = open_register_view
        self.open_cartelera_view = open_cartelera_view
        self.open_trabajador_view = open_trabajador_view 
        self.open_admin_view = open_admin_view

        # Crear los dos frames
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill='x', padx=20, pady=10)

        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Frame para el header
        current_dir = os.path.dirname(__file__)  # Obtiene el directorio actual
        logo_path = os.path.join(current_dir, "..", "images", "logo.png")  # Ruta correcta

        self.logo_image = Image.open(logo_path)  # Ajustamos la ruta aquí
        self.logo_image = self.logo_image.resize((100, 100))  # Redimensionar si es necesario
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        
        self.logo_label = ctk.CTkLabel(self.header_frame, image=self.logo_photo, text="")  # Corregido para evitar texto
        self.logo_label.pack(side="left", padx=10)

        self.app_name_label = ctk.CTkLabel(self.header_frame, text="CineMaster", font=("Arial", 24, "bold"))
        self.app_name_label.pack(side="left", padx=10)

        # Frame para los campos de login
        self.app_apatado_label = ctk.CTkLabel(self.login_frame, text="LOGIN", font=("Arial", 24, "bold"))
        self.app_apatado_label.pack(pady=20)

        self.email_label = ctk.CTkLabel(self.login_frame, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = ctk.CTkEntry(self.login_frame)
        self.email_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self.login_frame, text="Contraseña:")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        # Botón de inicio de sesión
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        # Botón para registrarse
        self.register_button = ctk.CTkButton(self.login_frame, text="¿No tienes una cuenta? Registrate", command=self.open_register)
        self.register_button.pack(pady=5)

    def login(self):
        # Obtener los datos de la entrada
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Validación del email
        if "@" not in email:
            messagebox.showerror("Error", "El correo electrónico debe contener '@'.")
            return  # No continuar con el login si el email es inválido

        # Crear una sesión de base de datos
        db = SessionLocal()

        # Llamamos al controlador para hacer login de cada tipo de usuario
        cliente = AuthController.login_cliente(db, email, password)
        if cliente:
            # Si las credenciales son correctas para un cliente
            messagebox.showinfo("Éxito", "Login como Cliente completado!")
            self.destroy()  # Cerrar ventana de login
            self.open_cartelera_view(cliente)  # Abrir la vista de cartelera
        else:
            # Si no es un cliente, intentamos autenticar como empleado
            empleado = AuthController.login_empleado(db, email, password)
            if empleado:
                # Si las credenciales son correctas para un empleado
                messagebox.showinfo("Éxito", "Login como Empleado completado")
                self.destroy()  # Cerrar ventana de login
                self.open_trabajador_view(empleado.Name)  # Abrir la vista de trabajador
            else:
                # Si no es un cliente ni un empleado, intentamos autenticar como administrador
                admin = AuthController.login_admin(db, email, password)
                if admin:
                    # Si las credenciales son correctas para un administrador
                    messagebox.showinfo("Éxito", "Login como Admin completado!")
                    self.destroy()  # Cerrar ventana de login
                    self.open_admin_view()  # Abrir la vista de administrador
                else:
                    # Si las credenciales son incorrectas
                    messagebox.showerror("Error", "email o contraseña Incorrecta.")
                    self.email_entry.delete(0, ctk.END)  # Limpiar el campo de email
                    self.password_entry.delete(0, ctk.END)  # Limpiar el campo de contraseña
                    self.email_entry.focus()  # Volver a enfocar el campo de email
                    self.password_entry.focus()  # Volver a enfocar el campo de contraseña

        db.close()  # Cerrar la sesión de la base de datos

    def open_register(self):
        # Abrir la ventana de registro
        self.open_register_view()  # Llamamos a la función pasada desde main.py
        self.quit()  # Usamos 'quit()' para salir del ciclo de eventos, en vez de 'destroy()'
