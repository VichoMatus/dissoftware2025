import customtkinter as ctk
from tkinter import messagebox

class RegisterView(ctk.CTk):
    def __init__(self, registration_service, open_login_view):
        super().__init__()
        self.title("Register")
        self.geometry("500x400")

        self.registration_service = registration_service
        self.open_login_view = open_login_view

        self.title_label = ctk.CTkLabel(self, text="REGISTRO", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)
        
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

        self.register_button = ctk.CTkButton(self, text="Registro", command=self.register)
        self.register_button.pack(pady=20)

    def register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        membership = 0  # Si en el futuro se usa membresía, pásala como parámetro

        # Validaciones básicas
        if "@" not in email:
            messagebox.showerror("Error", "El correo electrónico debe contener '@'.")
            return
        if len(password) < 4:
            messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.")
            return

        result = self.registration_service.register_cliente(name, email, password, membership)
        if result["success"]:
            messagebox.showinfo("Success", f"Cliente {result['cliente'].nombre} registrado exitosamente!")
            self.destroy()
        else:
            messagebox.showerror("Error", f"No se pudo registrar: {result['error']}")