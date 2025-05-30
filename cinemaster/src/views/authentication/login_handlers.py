from models.auth_controller import AuthController

class LoginHandler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, db, email, password):
        if self.next_handler:
            return self.next_handler.handle(db, email, password)
        return None, None

class ClienteLoginHandler(LoginHandler):
    def handle(self, db, email, password):
        cliente = AuthController.login_cliente(db, email, password)
        if cliente:
            return "cliente", cliente
        return super().handle(db, email, password)

class EmpleadoLoginHandler(LoginHandler):
    def handle(self, db, email, password):
        empleado = AuthController.login_empleado(db, email, password)
        if empleado:
            return "empleado", empleado
        return super().handle(db, email, password)

class AdminLoginHandler(LoginHandler):
    def handle(self, db, email, password):
        admin = AuthController.login_admin(db, email, password)
        if admin:
            return "admin", admin
        return super().handle(db, email, password)
