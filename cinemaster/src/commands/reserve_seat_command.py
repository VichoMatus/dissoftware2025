from models.database import Reserva, get_db, Reserva_asientos, HorarioAsientos
from sqlalchemy.orm import Session
import uuid

class ReserveSeatCommand:
    def __init__(self, client_id, id_funcion, seat_id):
        self.client_id = client_id
        self.id_funcion = id_funcion
        self.seat_id = seat_id

    def execute(self):
        db: Session = next(get_db())

        nueva_reserva = Reserva(
            client_id=self.client_id,
            id_funcion=self.id_funcion,
            id_promotions=1,
            employee_id=None
        )
        db.add(nueva_reserva)
        db.commit()
        db.refresh(nueva_reserva)

        horario_asiento = db.query(HorarioAsientos)\
            .filter(HorarioAsientos.horario_id == self.id_funcion,
                    HorarioAsientos.asiento_id == self.seat_id)\
            .first()

        if not horario_asiento:
            db.rollback()
            raise ValueError("El asiento no está asignado para este horario.")

        if not horario_asiento.Available:
            db.rollback()
            raise ValueError("El asiento no está disponible para este horario.")

        horario_asiento.Available = False
        db.add(horario_asiento)

        reserva_asiento = Reserva_asientos(
            reservationseat_id=str(uuid.uuid4()),
            reservation_id=nueva_reserva.reservation_id,
            ids_seats=self.seat_id
        )
        db.add(reserva_asiento)

        db.commit()
        db.refresh(nueva_reserva)

        # ✅ Precargar relaciones para evitar errores por sesión cerrada
        _ = nueva_reserva.client
        _ = nueva_reserva.funcion
        if nueva_reserva.funcion:
            _ = nueva_reserva.funcion.pelicula

        return nueva_reserva
