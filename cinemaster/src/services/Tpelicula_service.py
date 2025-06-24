from sqlalchemy.orm import Session
from models.database import Pelicula

class PeliculaService:
    @staticmethod
    def listar_peliculas(db: Session):
        return db.query(Pelicula).all()

    @staticmethod
    def crear_pelicula(db: Session, Title, Duration, Gender, Image_path):
        nueva = Pelicula(
            Title=Title,
            Duration=Duration,
            Gender=Gender,
            Image_path=Image_path
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def actualizar_pelicula(db: Session, id_pelicula, Title, Duration, Gender, Image_path):
        pelicula = db.query(Pelicula).filter(Pelicula.id_pelicula == id_pelicula).first()
        if pelicula:
            pelicula.Title = Title
            pelicula.Duration = Duration
            pelicula.Gender = Gender
            pelicula.Image_path = Image_path
            db.commit()
            return pelicula
        return None

    @staticmethod
    def eliminar_pelicula(db: Session, id_pelicula):
        pelicula = db.query(Pelicula).filter(Pelicula.id_pelicula == id_pelicula).first()
        if pelicula:
            db.delete(pelicula)
            db.commit()
            return True
        return False