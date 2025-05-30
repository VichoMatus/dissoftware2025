from models.database import Asiento, get_db
from models.seat import Seat
class ReservationSystem:
    def get_seat_by_id(self, seat_id):
        db = next(get_db())
        asiento_record = db.query(Asiento).filter(Asiento.ids_seats == seat_id).first()
        if asiento_record:
            return Seat(
                seat_id=asiento_record.ids_seats,
                row=getattr(asiento_record, "row", None),
                column=getattr(asiento_record, "column", None),
                status="Disponible"  # o determina según lógica real
            )
        else:
            return None