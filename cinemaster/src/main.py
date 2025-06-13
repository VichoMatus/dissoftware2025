import customtkinter as ctk
from views.authentication.login_view import LoginView
from views.authentication.register_view import RegisterView
from views.cartelera_view import MainView
from views.trabajador_view import ClienteView
from views.admin_view import AdminView
from services.empleado_service import EmpleadoService
from services.cliente_service import ClienteService
from database import db_session  # Ajusta el import según tu estructura real


def open_register_view():
    app = RegisterView(open_login_view)  # Crear la ventana de registro
    app.mainloop()

def open_login_view():
    app = LoginView(open_register_view, open_cartelera_view, open_trabajador_view,open_adimn_view)  # Crear la ventana de login
    app.mainloop()

def open_cartelera_view(cliente):
    app = MainView(cliente)  # Llamar sin pasarle parámetros
    app.mainloop()


def open_trabajador_view(employee_name):
    app = ClienteView(employee_name)
    app.mainloop()

def open_adimn_view():
    empleado_service = EmpleadoService(db_session)
    cliente_service = ClienteService(db_session)
    app = AdminView(empleado_service, cliente_service)
    app.mainloop()

if __name__ == "__main__":
    open_login_view()  # Inicia la ventana de login
