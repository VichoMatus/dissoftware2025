from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models.database import Reserva, Cliente, Funcion, Pelicula, Reserva_asientos, Asiento

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_reservation_details(reservation_id):
    db = SessionLocal()
    try:
        reserva = (
            db.query(Reserva)
            .filter(Reserva.reservation_id == reservation_id)
            .options(
                joinedload(Reserva.client),
                joinedload(Reserva.funcion),
                joinedload(Reserva.reserva_asientos).joinedload(Reserva_asientos.asiento)
            )
            .first()
        )
        if not reserva:
            return None

        cliente = reserva.client
        funcion = reserva.funcion
        asiento = reserva.reserva_asientos[0].asiento if reserva.reserva_asientos else None
        pelicula = db.query(Pelicula).filter(Pelicula.id_pelicula == funcion.id_pelicula).first() if funcion else None

        details = {
            "movie_name": pelicula.Title if pelicula else "N/A",
            "showtime_string": funcion.Schedule.strftime("%Y-%m-%d %H:%M") if funcion else "N/A",
            "seat": asiento.ids_seats if asiento else "N/A",
            "cliente_nombre": cliente.nombre if cliente else "N/A",
            "price": 12.0
        }
        return details
    finally:
        db.close()
