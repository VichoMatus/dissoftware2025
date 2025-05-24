from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
import copy

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'Cliente'  # Nombre de la tabla en la base de datos

    cliente_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    Email = Column(String, unique=True, index=True)
    Password = Column(String)
    Membership = Column(Boolean, default=False)
    Reservation_history = Column(String, default="")

    def __repr__(self):
        return f"<Cliente(cliente_id={self.cliente_id}, Name={self.nombre}, Email={self.Email}, Membership={self.Membership})>"
    
    def obtener_reservas_actuales(self):
        from datetime import datetime
        ahora = datetime.now()
        return [r for r in self.reservas if r.funcion and r.funcion.Schedule >= ahora]

    def obtener_historial_reservas(self):
        from datetime import datetime
        ahora = datetime.now()
        return [r for r in self.reservas if r.funcion and r.funcion.Schedule < ahora]

    def clone(self):
        """
        Clona el objeto Cliente para crear un nuevo cliente basado en este.
        Se hace una copia superficial y se resetea el cliente_id para evitar conflictos en la base.
        """
        # Copia superficial del objeto
        cliente_clonado = copy.copy(self)
        # Resetear la PK para que SQLAlchemy la asigne nueva al guardar
        cliente_clonado.cliente_id = None
        # Puedes limpiar otros atributos relacionados si quieres (ejemplo: historial)
        cliente_clonado.Reservation_history = ""
        # Retorna el nuevo objeto clonado listo para ser modificado y guardado
        return cliente_clonado
