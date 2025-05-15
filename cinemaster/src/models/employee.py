from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Empleado(Base):
    __tablename__ = 'Empleado'
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String(150))
    Name = Column(String(100))
    Password = Column(String(50))
