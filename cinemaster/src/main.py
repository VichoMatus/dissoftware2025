import customtkinter as ctk
from views.authentication.login_view import LoginView
from views.authentication.register_view import RegisterView
from views.cartelera_view import MainView
from views.trabajador_view import TrabajadorView
from views.admin_view import AdminView

# Importa los servicios
from views.authentication.auth_service import AuthService
from views.authentication.registration_service import RegistrationService

# Instancia los servicios una sola vez
auth_service = AuthService()
registration_service = RegistrationService()

def open_register_view():
    app = RegisterView(registration_service, open_login_view)
    app.mainloop()

def open_login_view():
    app = LoginView(
        auth_service,
        open_register_view,
        open_cartelera_view,
        open_trabajador_view,
        open_admin_view
    )
    app.mainloop()

def open_cartelera_view(cliente):
    app = MainView(cliente)
    app.mainloop()

def open_trabajador_view(employee_name):
    app = TrabajadorView(employee_name)
    app.mainloop()

def open_admin_view():
    app = AdminView()
    app.mainloop()

if __name__ == "__main__":
    open_login_view()