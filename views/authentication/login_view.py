import customtkinter as ctk

class LoginView(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self, text="Iniciar Sesión", font=("Arial", 24))
        self.title_label.grid(row=0, column=0, pady=10)

        self.username_label = ctk.CTkLabel(self, text="Nombre de usuario")
        self.username_label.grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=2, column=0, padx=10, pady=5)

        self.password_label = ctk.CTkLabel(self, text="Contraseña")
        self.password_label.grid(row=3, column=0, sticky="w", pady=5)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=4, column=0, padx=10, pady=5)

        self.login_button = ctk.CTkButton(self, text="Iniciar Sesión", command=self.login)
        self.login_button.grid(row=5, column=0, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        print(f"Iniciando sesión con {username} y {password}")

