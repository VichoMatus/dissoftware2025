from sqlalchemy.orm import Session
from models.database import Reserva
import requests


class ReservaService:
    @staticmethod
    def listar_reservas(db: Session):
        return db.query(Reserva).all()

    @staticmethod
    def crear_reserva(db: Session, client_id: int, id_funcion: int, employee_id: int):
        nueva = Reserva(
            client_id=client_id,
            id_funcion=id_funcion,
            employee_id=employee_id
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def actualizar_reserva(db: Session, reservation_id: int, client_id: int, id_funcion: int, employee_id: int):
        reserva = db.query(Reserva).filter(Reserva.reservation_id == reservation_id).first()
        if reserva:
            reserva.client_id = client_id
            reserva.id_funcion = id_funcion
            reserva.employee_id = employee_id
            db.commit()
            return reserva
        return None

    @staticmethod
    def eliminar_reserva(db: Session, reservation_id: int):
        reserva = db.query(Reserva).filter(Reserva.reservation_id == reservation_id).first()
        if reserva:
            db.delete(reserva)
            db.commit()
            return True
        return False

class ReservaAPIService:
    API_URL = "http://127.0.0.1:8000/reservas/"

    def listar_reservas(self):
        response = requests.get(self.API_URL)
        response.raise_for_status()
        return response.json()

    def crear_reserva(self, client_id: int, id_funcion: int, employee_id: int):
        data = {
            "client_id": client_id,
            "id_funcion": id_funcion,
            "employee_id": employee_id
        }
        response = requests.post(self.API_URL, json=data)
        response.raise_for_status()
        return response.json()

    def actualizar_reserva(self, reservation_id, client_id, id_funcion, employee_id, id_promotions=None):
        data = {
            "client_id": client_id,
            "id_funcion": id_funcion,
            "employee_id": employee_id,
            "id_promotions": id_promotions
        }
        response = requests.put(f"{self.API_URL}{reservation_id}", json=data)
        response.raise_for_status()
        return response.json()

    def eliminar_reserva(self, reservation_id):
        response = requests.delete(f"{self.API_URL}{reservation_id}")
        response.raise_for_status()
        return response.json()