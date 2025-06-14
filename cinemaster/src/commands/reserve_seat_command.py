from models.database import Reserva, get_db, Reserva_asientos, HorarioAsientos
from sqlalchemy.orm import Session
import uuid
from utils.decorators import medir_tiempo
from models.seat import Seat

class ReserveSeatCommand:
    def __init__(self, client_id, id_funcion, seat_id):
        self.client_id = client_id
        self.id_funcion = id_funcion
        self.seat_id = seat_id
    @medir_tiempo
    def execute(self):
        db: Session = next(get_db())

        # Obtener datos asiento desde BD
        horario_asiento = db.query(HorarioAsientos)\
            .filter(HorarioAsientos.horario_id == self.id_funcion,
                    HorarioAsientos.asiento_id == self.seat_id)\
            .first()

        if not horario_asiento:
            db.rollback()
            raise ValueError("El asiento no está asignado para este horario.")

        # Crear objeto Seat y Proxy
        seat_obj = Seat(
            seat_id=horario_asiento.asiento.ids_seats,
            row=getattr(horario_asiento.asiento, "row", None),
            column=getattr(horario_asiento.asiento, "column", None),
            status="Disponible" if horario_asiento.Available else "Reservado"
        )

        # Si proxy reserva en memoria, seguimos con DB
        nueva_reserva = Reserva(
            client_id=self.client_id,
            id_funcion=self.id_funcion,
            id_promotions=1,
            employee_id=None
        )
        db.add(nueva_reserva)
        db.commit()
        db.refresh(nueva_reserva)

        # Marcar asiento como no disponible en BD
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

        # Precargar relaciones
        _ = nueva_reserva.client
        _ = nueva_reserva.funcion
        if nueva_reserva.funcion:
            _ = nueva_reserva.funcion.pelicula

        return nueva_reserva