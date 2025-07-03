from sqlalchemy.orm import Session
from models.database import Funcion
import requests

class FuncionService:
    @staticmethod
    def listar_funciones(db: Session):
        return db.query(Funcion).all()

    @staticmethod
    def crear_funcion(db: Session, id_pelicula, employee_id, Schedule):
        nueva = Funcion(
            id_pelicula=id_pelicula,
            employee_id=employee_id,
            Schedule=Schedule
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def actualizar_funcion(db: Session, id_funcion, id_pelicula, employee_id, Schedule):
        funcion = db.query(Funcion).filter(Funcion.id_funcion == id_funcion).first()
        if funcion:
            funcion.id_pelicula = id_pelicula
            funcion.employee_id = employee_id
            funcion.Schedule = Schedule
            db.commit()
            return funcion
        return None

    @staticmethod
    def eliminar_funcion(db: Session, id_funcion):
        funcion = db.query(Funcion).filter(Funcion.id_funcion == id_funcion).first()
        if funcion:
            db.delete(funcion)
            db.commit()
            return True
        return False

class FuncionAPIService:
    API_URL = "http://127.0.0.1:8000/funciones/"

    def listar_funciones(self):
        response = requests.get(self.API_URL)
        response.raise_for_status()
        return response.json()

    def obtener_peliculas_disponibles(self):
        """Obtiene lista de películas disponibles para dropdowns"""
        response = requests.get(f"{self.API_URL}peliculas-disponibles")
        response.raise_for_status()
        return response.json()

    def crear_funcion(self, id_pelicula, employee_id, Schedule):
        data = {
            "id_pelicula": id_pelicula,
            "employee_id": employee_id,
            "Schedule": Schedule  # Debe ser string en formato ISO (ej: "2024-07-01T20:00:00")
        }
        response = requests.post(self.API_URL, json=data)
        response.raise_for_status()
        return response.json()

    def actualizar_funcion(self, id_funcion, id_pelicula, employee_id, Schedule):
        data = {
            "id_pelicula": id_pelicula,
            "employee_id": employee_id,
            "Schedule": Schedule
        }
        response = requests.put(f"{self.API_URL}{id_funcion}", json=data)
        response.raise_for_status()
        return response.json()

    def eliminar_funcion(self, id_funcion):
        response = requests.delete(f"{self.API_URL}{id_funcion}")
        response.raise_for_status()
        return response.json()