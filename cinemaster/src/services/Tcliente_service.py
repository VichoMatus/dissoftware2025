from sqlalchemy.orm import Session
from models.database import Cliente
import requests

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
    
    
class ClienteAPIService:
    API_URL = "http://127.0.0.1:8000/clientes/"

    def listar_clientes(self):
        response = requests.get(self.API_URL)
        response.raise_for_status()
        return response.json()

    def crear_cliente(self, nombre, email, password):
        data = {
            "nombre": nombre,
            "Email": email,
            "Password": password
        }
        response = requests.post(self.API_URL, json=data)
        response.raise_for_status()
        return response.json()

    def actualizar_cliente(self, cliente_id, nombre, email, password):
        data = {
            "nombre": nombre,
            "Email": email,
            "Password": password
        }
        response = requests.put(f"{self.API_URL}{cliente_id}", json=data)
        response.raise_for_status()
        return response.json()

    def eliminar_cliente(self, cliente_id):
        response = requests.delete(f"{self.API_URL}{cliente_id}")
        response.raise_for_status()
        return response.json()