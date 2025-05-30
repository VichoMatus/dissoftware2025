from sqlalchemy import Column, Integer, String, Boolean  # Asegúrate de importar Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Administrador(Base):
    __tablename__ = 'Administrador'  # Nombre de la tabla en la base de datos

    Admin_id = Column(Integer, primary_key=True, index=True)  # Clave primaria
    nombre = Column(String, index=True)  # Nombre del cliente
    Email = Column(String, unique=True, index=True)  # Email único del cliente
    Password = Column(String)  # Contraseña en formato hasheado