from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import copy

Base = declarative_base()

class Empleado(Base):
    __tablename__ = 'Empleado'
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String(150))
    Name = Column(String(100))
    Password = Column(String(50))

    def clone(self):
        """
        Clona el objeto Empleado para crear un nuevo empleado basado en este.
        Se hace una copia superficial y se resetea el employee_id para evitar conflictos en la base.
        """
        # Copia superficial del objeto
        empleado_clonado = copy.copy(self)
        # Resetear la PK para que SQLAlchemy la asigne nueva al guardar
        empleado_clonado.employee_id = None
        # Retorna el nuevo objeto clonado listo para ser modificado y guardado
        return empleado_clonado
