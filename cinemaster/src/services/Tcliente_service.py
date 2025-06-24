from sqlalchemy.orm import Session
from models.database import Cliente

class ClienteService:
    @staticmethod
    def listar_clientes(db: Session):
        return db.query(Cliente).all()

    @staticmethod
    def crear_cliente(db: Session, nombre, email, password):
        nuevo = Cliente(nombre=nombre, Email=email, Password=password, Reservation_history="", Membership=False)
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    @staticmethod
    def actualizar_cliente(db: Session, cliente_id, nombre, email, password):
        cliente = db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()
        if cliente:
            cliente.nombre = nombre
            cliente.Email = email
            cliente.Password = password
            db.commit()
            return cliente
        return None

    @staticmethod
    def eliminar_cliente(db: Session, cliente_id):
        cliente = db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()
        if cliente:
            db.delete(cliente)
            db.commit()
            return True
        return False