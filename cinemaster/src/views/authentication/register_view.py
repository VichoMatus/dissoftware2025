import customtkinter as ctk
from tkinter import messagebox
from models.database import SessionLocal
from models.auth_controller import AuthController

class RegisterView(ctk.CTk):
    def __init__(self, open_login_view):
        super().__init__()
        self.title("Register")
        self.geometry("500x400")

        self.open_login_view = open_login_view

        # Título "REGISTRO" en grande
        self.title_label = ctk.CTkLabel(self, text="REGISTRO", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)  # Añadimos espacio debajo del título para separarlo de los demás elementos
        # Campos de registro
        self.name_label = ctk.CTkLabel(self, text="Nombre:")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady=5)

        self.email_label = ctk.CTkLabel(self, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self, text="Contraseña:")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)

        # Campo de Membresía (comentado)
        # self.membership_label = ctk.CTkLabel(self, text="Membresía:")
        # self.membership_label.pack(pady=5)
        # self.membership_var = ctk.BooleanVar()
        # self.membership_checkbox = ctk.CTkCheckBox(self, text="¿Tienes membresía?", variable=self.membership_var)
        # self.membership_checkbox.pack(pady=5)

        # Botón de registro
        self.register_button = ctk.CTkButton(self, text="Registro", command=self.register)
        self.register_button.pack(pady=20)

    def register(self):
        # Obtener los datos de la entrada
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        membership = 0  # Membresía comentada, no se utiliza ahora

        # Validaciones
        if "@" not in email:
            messagebox.showerror("Error", "El correo electrónico debe contener '@'.")
            return
        if len(password) < 4:
            messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.")
            return

        # Crear una sesión de base de datos
        db = SessionLocal()

        try:
            # Intentamos registrar al cliente
            cliente = AuthController.register_cliente(db, name, email, password, membership)
            
            # Si el registro fue exitoso, mostramos el mensaje de éxito
            messagebox.showinfo("Success", f"Cliente {cliente.nombre} registrado exitosamente!")

            # Después de registrar, volvemos a la ventana de login
            self.open_login_view()  # Volver a la vista de login
            self.destroy()  # Cerrar la ventana de registro
        except Exception as e:
            # Si ocurre un error (por ejemplo, email duplicado), mostramos el mensaje de error
            messagebox.showerror("Error", f"No se pudo registrar: {str(e)}")
        finally:
            # Cerramos la sesión de la base de datos
            db.close()
