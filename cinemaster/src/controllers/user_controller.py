from models.cliente import Cliente
from sqlalchemy.orm import Session

class UserController:
    def __init__(self, db_session: Session):
        self.db = db_session

    def clonar_cliente(self, cliente_id_existente):
        # Buscar cliente existente
        cliente_original = self.db.query(Cliente).filter(Cliente.cliente_id == cliente_id_existente).first()
        if not cliente_original:
            raise ValueError("Cliente original no encontrado")

        # Clonar el cliente
        nuevo_cliente = cliente_original.clone()

        # Modificar datos que deben ser únicos o requeridos
        nuevo_cliente.Email = None  # O pedir nuevo email
        nuevo_cliente.Password = None  # O asignar contraseña temporal o vacía
        nuevo_cliente.Membership = False  # Por defecto sin membresía

        # Guardar nuevo cliente en la base de datos
        self.db.add(nuevo_cliente)
        self.db.commit()
        self.db.refresh(nuevo_cliente)

        return nuevo_cliente
