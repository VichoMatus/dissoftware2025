from sqlalchemy import Column, Integer, String, Boolean  # Asegúrate de importar Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'Cliente'  # Nombre de la tabla en la base de datos

    cliente_id = Column(Integer, primary_key=True, index=True)  # Clave primaria
    nombre = Column(String, index=True)  # Nombre del cliente
    Email = Column(String, unique=True, index=True)  # Email único del cliente
    Password = Column(String)  # Contraseña en formato hasheado
    Membership = Column(Boolean, default=False)  # Estado de la membresía
    Reservation_history = Column(String, default="")  # Historial de reservas

    def __repr__(self):
        return f"<Cliente(cliente_id={self.cliente_id}, Name={self.Name}, Email={self.Email}, Membership={self.Membership})>"
