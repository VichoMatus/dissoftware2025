from views.authentication.login_view import LoginView
from views.authentication.register_view import RegisterView
from views.cartelera_view import MainView
from views.trabajador_view import ClienteView
from views.admin_view import AdminView
from views.authentication.auth_service import AuthService
from views.authentication.registration_service import RegistrationService

class AppController:
    def __init__(self):
        self.auth_service = AuthService()
        self.registration_service = RegistrationService()   
    def start(self):
        self.open_login_view()

    def open_register_view(self):
        app = RegisterView(self.registration_service, self.open_login_view)
        app.mainloop()

    def open_login_view(self):
        app = LoginView(
            self.auth_service,
            self.open_register_view,
            self.open_cartelera_view,
            self.open_trabajador_view,
            self.open_admin_view
        )
        app.mainloop()

    def open_cartelera_view(self, cliente):
        app = MainView(cliente)
        app.mainloop()

    def open_trabajador_view(self, employee_name):
        app = ClienteView(employee_name)
        app.mainloop()

    def open_admin_view(self):
        app = AdminView()
        app.mainloop()