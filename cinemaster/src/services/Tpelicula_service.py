from sqlalchemy.orm import Session
from models.database import Pelicula
import requests

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
    
class PeliculaAPIService:
    API_URL = "http://127.0.0.1:8000/peliculas/"

    def listar_peliculas(self):
        response = requests.get(self.API_URL)
        response.raise_for_status()
        return response.json()

    def crear_pelicula(self, Title, Duration, Gender, Image_path):
        data = {
            "Title": Title,
            "Duration": Duration,
            "Gender": Gender,
            "Image_path": Image_path
        }
        response = requests.post(self.API_URL, json=data)
        response.raise_for_status()
        return response.json()

    def actualizar_pelicula(self, id_pelicula, Title, Duration, Gender, Image_path):
        data = {
            "Title": Title,
            "Duration": Duration,
            "Gender": Gender,
            "Image_path": Image_path
        }
        response = requests.put(f"{self.API_URL}{id_pelicula}", json=data)
        response.raise_for_status()
        return response.json()

    def eliminar_pelicula(self, id_pelicula):
        response = requests.delete(f"{self.API_URL}{id_pelicula}")
        response.raise_for_status()
        return response.json()