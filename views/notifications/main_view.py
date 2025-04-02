import customtkinter as ctk
from views.login_view import LoginView

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cine Management System")
        self.geometry("600x400")

        # Mostramos la vista de inicio de sesión por defecto
        self.login_view = LoginView(self)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
