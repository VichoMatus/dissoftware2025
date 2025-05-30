import customtkinter as ctk
from tkinter import messagebox
from .login_handlers import ClienteLoginHandler, EmpleadoLoginHandler, AdminLoginHandler
from models.database import SessionLocal
from PIL import Image, ImageTk
from utils.decorators import medir_tiempo
import os

class LoginView(ctk.CTk):
    def __init__(self, open_register_view, open_cartelera_view, open_trabajador_view, open_admin_view):
        super().__init__()
        self.title("Login")
        self.geometry("1280x800")

        self.open_register_view = open_register_view
        self.open_cartelera_view = open_cartelera_view
        self.open_trabajador_view = open_trabajador_view 
        self.open_admin_view = open_admin_view

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill='x', padx=20, pady=10)

        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(fill='both', expand=True, padx=20, pady=10)

        current_dir = os.path.dirname(__file__)
        logo_path = os.path.join(current_dir, "..", "images", "logo.png")
        self.logo_image = Image.open(logo_path).resize((100, 100))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        
        self.logo_label = ctk.CTkLabel(self.header_frame, image=self.logo_photo, text="")
        self.logo_label.pack(side="left", padx=10)

        self.app_name_label = ctk.CTkLabel(self.header_frame, text="CineMaster", font=("Arial", 24, "bold"))
        self.app_name_label.pack(side="left", padx=10)

        self.app_apartado_label = ctk.CTkLabel(self.login_frame, text="LOGIN", font=("Arial", 24, "bold"))
        self.app_apartado_label.pack(pady=20)

        self.email_label = ctk.CTkLabel(self.login_frame, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = ctk.CTkEntry(self.login_frame)
        self.email_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self.login_frame, text="Contraseña:")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = ctk.CTkButton(self.login_frame, text="¿No tienes una cuenta? Regístrate", command=self.open_register)
        self.register_button.pack(pady=5)

    @medir_tiempo
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if "@" not in email:
            messagebox.showerror("Error", "El correo electrónico debe contener '@'.")
            return

        db = SessionLocal()

        # Patron: Chain of Responsibility
        handler_chain = ClienteLoginHandler(
            EmpleadoLoginHandler(
                AdminLoginHandler()
            )
        )

        tipo_usuario, usuario = handler_chain.handle(db, email, password)

        if tipo_usuario == "cliente":
            messagebox.showinfo("Éxito", "Login como Cliente completado!")
            self.destroy()
            self.open_cartelera_view(usuario)

        elif tipo_usuario == "empleado":
            messagebox.showinfo("Éxito", "Login como Empleado completado")
            self.destroy()
            self.open_trabajador_view(usuario.Name)

        elif tipo_usuario == "admin":
            messagebox.showinfo("Éxito", "Login como Admin completado!")
            self.destroy()
            self.open_admin_view()

        else:
            messagebox.showerror("Error", "Email o contraseña incorrecta.")
            self.email_entry.delete(0, ctk.END)
            self.password_entry.delete(0, ctk.END)
            self.email_entry.focus()
            self.password_entry.focus()

        db.close()

    def open_register(self):
        self.open_register_view()
        self.quit()