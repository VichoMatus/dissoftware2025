from sqlalchemy.orm import Session
from models.database import Funcion

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