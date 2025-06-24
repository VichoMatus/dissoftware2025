from sqlalchemy.orm import Session
from models.database import Reserva

class ReservaService:
    @staticmethod
    def listar_reservas(db: Session):
        return db.query(Reserva).all()

    @staticmethod
    def crear_reserva(db: Session, client_id, id_funcion, id_promotions, employee_id):
        nueva = Reserva(
            client_id=client_id,
            id_funcion=id_funcion,
            id_promotions=id_promotions,
            employee_id=employee_id
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def actualizar_reserva(db: Session, reservation_id, client_id, id_funcion, id_promotions, employee_id):
        reserva = db.query(Reserva).filter(Reserva.reservation_id == reservation_id).first()
        if reserva:
            reserva.client_id = client_id
            reserva.id_funcion = id_funcion
            reserva.id_promotions = id_promotions
            reserva.employee_id = employee_id
            db.commit()
            return reserva
        return None

    @staticmethod
    def eliminar_reserva(db: Session, reservation_id):
        reserva = db.query(Reserva).filter(Reserva.reservation_id == reservation_id).first()
        if reserva:
            db.delete(reserva)
            db.commit()
            return True
        return False