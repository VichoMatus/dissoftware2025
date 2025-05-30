from models.database import get_db
from sqlalchemy.orm import Session
from models.database import Pelicula, Horario, Asiento, HorarioAsientos
from datetime import datetime

def create_40_seats_for_showtime(db_session, horario_id):
    """
    Crea 40 asientos (5 filas x 8 columnas) para el horario dado.
    Los asientos serán etiquetados de la siguiente forma: A1, A2, ..., E8.
    """
    seat_ids = [f'{chr(65 + i)}{j+1}' for i in range(5) for j in range(8)]  # A1, A2, ..., E8

    for seat_id in seat_ids:
        existing_seat = db_session.query(Asiento).filter(Asiento.ids_seats == seat_id).first()

        if not existing_seat:
            # Crear asiento sin Available (ya no está en Asiento)
            new_seat = Asiento(ids_seats=seat_id)
            db_session.add(new_seat)
            db_session.commit()

        # Crear la relación con horario_asientos y poner Available=True
        existing_relation = db_session.query(HorarioAsientos).filter(
            HorarioAsientos.horario_id == horario_id,
            HorarioAsientos.asiento_id == seat_id
        ).first()

        if not existing_relation:
            horario_asiento = HorarioAsientos(
                horario_id=horario_id,
                asiento_id=seat_id,
                Available=True  # Asiento disponible para ese horario
            )
            db_session.add(horario_asiento)
            db_session.commit()

    print(f"Se han creado 40 asientos para el horario con ID {horario_id}.")

def create_movie_with_seats(db_session, title, gender, duration, image_path, horarios=[]):
    """
    Crea una película y asigna los horarios y 40 asientos para cada horario.
    """
    new_movie = Pelicula(Title=title, Gender=gender, Duration=duration, Image_path=image_path)
    db_session.add(new_movie)
    db_session.commit()
    db_session.refresh(new_movie)

    if horarios:
        for horario_fecha in horarios:
            new_horario = Horario(fecha=horario_fecha, pelicula_id=new_movie.id_pelicula)
            db_session.add(new_horario)
            db_session.commit()
            db_session.refresh(new_horario)

            create_40_seats_for_showtime(db_session, new_horario.id)

    return new_movie

def get_all_movies(session):
    return session.query(Pelicula).all()

def insert_sample_data():
    db: Session = next(get_db())

    horarios_deadpool = [
        datetime(2025, 5, 1, 14, 30),
        datetime(2025, 5, 1, 18, 0),
        datetime(2025, 5, 2, 14, 30),
        datetime(2025, 5, 2, 18, 0),
        datetime(2025, 5, 3, 14, 30),
        datetime(2025, 5, 3, 18, 0),
    ]
    horarios_paranorman = [
        datetime(2025, 5, 1, 13, 15),
        datetime(2025, 5, 1, 17, 0),
        datetime(2025, 5, 2, 14, 30),
        datetime(2025, 5, 2, 18, 0),
        datetime(2025, 5, 3, 15, 45),
        datetime(2025, 5, 3, 19, 0),
    ]
    horarios_avatar = [
        datetime(2025, 5, 1, 12, 0),
        datetime(2025, 5, 1, 15, 45),
        datetime(2025, 5, 2, 14, 30),
        datetime(2025, 5, 2, 18, 0),
        datetime(2025, 5, 3, 14, 30),
        datetime(2025, 5, 3, 18, 0),
    ]
    horarios_era_de_hielo = [
        datetime(2025, 5, 1, 14, 30),
        datetime(2025, 5, 1, 18, 0),
        datetime(2025, 5, 2, 11, 30),
        datetime(2025, 5, 2, 15, 35),
        datetime(2025, 5, 3, 14, 30),
        datetime(2025, 5, 3, 20, 15),
        datetime(2025, 5, 4, 14, 30),
        datetime(2025, 5, 4, 16, 50),
    ]
    horarios_valiente = [
        datetime(2025, 5, 1, 14, 30),
        datetime(2025, 5, 1, 17, 0),
        datetime(2025, 5, 2, 12, 30),
        datetime(2025, 5, 2, 18, 45),
        datetime(2025, 5, 3, 15, 30),
        datetime(2025, 5, 3, 19, 0),
    ]

    create_movie_with_seats(db, "Deadpool 3", "Acción", 120,"cinemaster/src/views/images/Deadpool 3.jpg" ,horarios=horarios_deadpool)
    create_movie_with_seats(db, "ParaNorman", "Comedia y Terror", 100,"cinemaster/src/views/images/ParaNorman.jpg", horarios=horarios_paranorman)
    create_movie_with_seats(db, "Avatar", "Ciencia Ficcion", 150,"cinemaster/src/views/images/Avatar.jpg" ,horarios=horarios_avatar)
    create_movie_with_seats(db, "La Era del Hielo 5", "Infantil", 150,"cinemaster/src/views/images/La Era del Hielo 5.jpg" ,horarios=horarios_era_de_hielo)
    create_movie_with_seats(db, "Valiente", "Ciencia Ficción", 150,"cinemaster/src/views/images/Valiente.jpg" ,horarios=horarios_valiente)

    db.close()

    print("Películas insertadas con éxito.")

#insert_sample_data()