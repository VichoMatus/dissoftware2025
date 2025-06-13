from models.cliente import Cliente
from sqlalchemy.orm import Session
from typing import List, Optional, Protocol

class IClienteCRUD(Protocol):
    def agregar_cliente(self, nombre: str, email: str, password: str, membresia: bool) -> Cliente: ...
    def listar_clientes(self) -> List[Cliente]: ...
    def obtener_cliente(self, cliente_id: int) -> Optional[Cliente]: ...
    def actualizar_cliente(self, cliente_id: int, nombre: str, email: str, password: str, membresia: bool) -> Optional[Cliente]: ...
    def eliminar_cliente(self, cliente_id: int) -> bool: ...

class ClienteService(IClienteCRUD):
    def __init__(self, db_session: Session):
        self.db = db_session

    def agregar_cliente(self, nombre: str, email: str, password: str, membresia: bool) -> Cliente:
        cliente = Cliente(nombre=nombre, Email=email, Password=password, Reservation_history="", Membership=membresia)
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def listar_clientes(self) -> List[Cliente]:
        return self.db.query(Cliente).all()

    def obtener_cliente(self, cliente_id: int) -> Optional[Cliente]:
        return self.db.query(Cliente).get(cliente_id)

    def actualizar_cliente(self, cliente_id: int, nombre: str, email: str, password: str, membresia: bool) -> Optional[Cliente]:
        cl = self.db.query(Cliente).get(cliente_id)
        if cl:
            cl.nombre = nombre
            cl.Email = email
            cl.Password = password
            cl.Membership = membresia
            self.db.commit()
            self.db.refresh(cl)
            return cl
        return None

    def eliminar_cliente(self, cliente_id: int) -> bool:
        cl = self.db.query(Cliente).get(cliente_id)
        if cl:
            self.db.delete(cl)
            self.db.commit()
            return True
        return False