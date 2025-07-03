from models.database import SessionLocal
from models.auth_controller import AuthController

class RegistrationService:
    def __init__(self, session_factory=SessionLocal, controller=AuthController):
        self.session_factory = session_factory
        self.controller = controller

    def register_cliente(self, name, email, password, membership):
        db = self.session_factory()
        try:
            cliente = self.controller.register_cliente(db, name, email, password, membership)
            return {"success": True, "cliente": cliente}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            db.close()