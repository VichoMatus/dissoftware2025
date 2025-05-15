from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Crear la base de datos y la conexión
DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/nombre_base_de_datos"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True para ver las consultas SQL en la consola
Base = declarative_base()

# Definición de los modelos

class Sala(Base):
    __tablename__ = 'Sala'

    id_Hall = Column(Integer, primary_key=True, autoincrement=True)
    Capacity = Column(Integer)
    Type = Column(String(100))

    # Relacionar con Asiento
    asientos = relationship("Asiento", back_populates="sala")


class Asiento(Base):
    __tablename__ = 'Asiento'

    ids_seats = Column(String(50), primary_key=True)
    id_Hall = Column(Integer, ForeignKey('Sala.id_Hall'))
    Available = Column(Boolean)

    # Relacionar con Sala
    sala = relationship("Sala", back_populates="asientos")


class Empleado(Base):
    __tablename__ = 'Empleado'

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String(150))
    Name = Column(String(100))
    Password = Column(String(50))

    # Relacionar con Función y Reserva
    funciones = relationship("Funcion", back_populates="empleado")
    reservas = relationship("Reserva", back_populates="empleado")


class Pelicula(Base):
    __tablename__ = 'Pelicula'

    id_pelicula = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(255))
    Duration = Column(Integer)
    Gender = Column(String(50))

    # Relacionar con Funcion
    funciones = relationship("Funcion", back_populates="pelicula")


class Promociones(Base):
    __tablename__ = 'Promociones'

    id_promotions = Column(Integer, primary_key=True, autoincrement=True)
    Type = Column(String(50))
    Membership = Column(DECIMAL(5, 2))

    # Relacionar con Reserva
    reservas = relationship("Reserva", back_populates="promocion")


class Cliente(Base):
    __tablename__ = 'Cliente'

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100))
    Email = Column(String(150))
    Reservation_history = Column(String)
    Membership = Column(Boolean)
    Password = Column(String(50))

    # Relacionar con Reserva
    reservas = relationship("Reserva", back_populates="cliente")


class Reserva(Base):
    __tablename__ = 'Reserva'

    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('Cliente.client_id'))
    id_funcion = Column(Integer, ForeignKey('Funcion.id_funcion'))
    id_promotions = Column(Integer, ForeignKey('Promociones.id_promotions'))
    employee_id = Column(Integer, ForeignKey('Empleado.employee_id'))

    # Relacionar con Cliente, Empleado, Funcion y Promociones
    cliente = relationship("Cliente", back_populates="reservas")
    empleado = relationship("Empleado", back_populates="reservas")
    funcion = relationship("Funcion", back_populates="reservas")
    promocion = relationship("Promociones", back_populates="reservas")
    reserva_asientos = relationship("ReservaAsientos", back_populates="reserva")


class Funcion(Base):
    __tablename__ = 'Funcion'

    id_funcion = Column(Integer, primary_key=True, autoincrement=True)
    id_pelicula = Column(Integer, ForeignKey('Pelicula.id_pelicula'))
    employee_id = Column(Integer, ForeignKey('Empleado.employee_id'))
    Schedule = Column(Date)

    # Relacionar con Pelicula y Empleado
    pelicula = relationship("Pelicula", back_populates="funciones")
    empleado = relationship("Empleado", back_populates="funciones")
    reservas = relationship("Reserva", back_populates="funcion")


class ReservaAsientos(Base):
    __tablename__ = 'Reserva_asientos'

    reservationseat_id = Column(String(80), primary_key=True)
    reservation_id = Column(Integer, ForeignKey('Reserva.reservation_id'))
    ids_seats = Column(String(50), ForeignKey('Asiento.ids_seats'))

    # Relacionar con Reserva y Asiento
    reserva = relationship("Reserva", back_populates="reserva_asientos")
    asiento = relationship("Asiento")


# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una instancia de sesión
session = SessionLocal()

# Ejemplo de consulta
# Obtener todas las películas
peliculas = session.query(Pelicula).all()
for pelicula in peliculas:
    print(pelicula.Title)
