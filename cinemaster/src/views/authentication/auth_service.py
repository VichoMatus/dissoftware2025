from .login_handlers import ClienteLoginHandler, EmpleadoLoginHandler, AdminLoginHandler
from models.database import SessionLocal
from utils.decorators import medir_tiempo

class AuthService:
    def __init__(self, session_factory=SessionLocal, handler_chain=None):
        self.session_factory = session_factory
        if handler_chain is None:
            # Chain of Responsibility configurada por defecto, pero inyectable
            self.handler_chain = ClienteLoginHandler(
                EmpleadoLoginHandler(
                    AdminLoginHandler()
                )
            )
        else:
            self.handler_chain = handler_chain

    @medir_tiempo
    def authenticate(self, email, password):
        db = self.session_factory()
        try:
            tipo_usuario, usuario = self.handler_chain.handle(db, email, password)
            if tipo_usuario in ["cliente", "empleado", "admin"]:
                return {"success": True, "tipo_usuario": tipo_usuario, "usuario": usuario}
            else:
                return {"success": False}
        finally:
            db.close()