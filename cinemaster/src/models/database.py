from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Base declarativa de SQLAlchemy
Base = declarative_base()

# Configuración de la conexión con la base de datos
DATABASE_URL = "sqlite:///./test.db"  # Usa SQLite para pruebas
# DATABASE_URL = "mysql+mysqlconnector://user:password@localhost:3306/database_name"  # Usa MySQL en producción

# Crear la conexión a la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definición de las clases que representan las tablas

class Sala(Base):
    __tablename__ = "Sala"
    id_Hall = Column(Integer, primary_key=True, index=True)
    Capacity = Column(Integer)
    Type = Column(String(100))

class Asiento(Base):
    __tablename__ = "Asiento"
    ids_seats = Column(String(50), primary_key=True)
    id_Hall = Column(Integer, ForeignKey("Sala.id_Hall"))

    sala = relationship("Sala")
    horarios = relationship("Horario", secondary="horario_asientos", overlaps="asientos,horario_asientos")

class Administrador(Base):
    __tablename__ = 'Administrador'  # Nombre de la tabla en la base de datos   
    Admin_id = Column(Integer,primary_key=True,index=True)  # Clave primaria
    nombre = Column(String, nullable=False)  # Nombre del cliente
    Email = Column(String, unique=True, nullable=False)  # Email único del cliente
    Password = Column(String, nullable=False)  # Contraseña en formato hasheado

class Empleado(Base):
    __tablename__ = "Empleado"
    employee_id = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100))
    Email = Column(String(150))
    Password = Column(String(50))

class Cliente(Base):
    __tablename__ = "Cliente"
    cliente_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    Email = Column(String, unique=True, nullable=False)
    Membership = Column(Boolean, default=False)
    Reservation_history = Column(String, default="")
    Password = Column(String, nullable=False)

    reservas = relationship("Reserva", back_populates="client")

    def __repr__(self):
        return f"<Cliente(cliente_id={self.cliente_id}, Name={self.nombre}, Email={self.Email}, Membership={self.Membership})>"


class Pelicula(Base):
    __tablename__ = 'Pelicula'  # Nombre de la tabla en la base de datos
    id_pelicula = Column(Integer, primary_key=True, index=True)
    Title = Column(String(255), nullable=False)
    Duration = Column(Integer, nullable=False)
    Gender = Column(String(50), nullable=True)
    Image_path = Column(String(500), nullable=False)

    horarios = relationship('Horario', back_populates='pelicula')


class Horario(Base):
    __tablename__ = 'Horario'
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False)  # Almacena la fecha y hora del horario
    pelicula_id = Column(Integer, ForeignKey('Pelicula.id_pelicula'))  # Relación con la película
    pelicula = relationship('Pelicula', back_populates='horarios')
    asientos = relationship("Asiento", secondary="horario_asientos", overlaps="horarios,horario_asientos")


class HorarioAsientos(Base):
    __tablename__ = 'horario_asientos'
    horario_id = Column(Integer, ForeignKey('Horario.id'), primary_key=True)
    asiento_id = Column(String(50), ForeignKey('Asiento.ids_seats'), primary_key=True)
    Available = Column(Boolean, default=True)
    # Relación entre Horario y Asiento
    horario = relationship("Horario", backref="horario_asientos", overlaps="asientos,horarios")
    asiento = relationship("Asiento", backref="horario_asientos", overlaps="asientos,horarios")


class Promociones(Base):
    __tablename__ = "Promociones"
    id_promotions = Column(Integer, primary_key=True, index=True)
    Type = Column(String(50))
    Membership = Column(Integer)

class Reserva(Base):
    __tablename__ = "Reserva"
    reservation_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("Cliente.cliente_id"))
    id_funcion = Column(Integer, ForeignKey("Funcion.id_funcion"))  # Corregido aquí
    id_promotions = Column(Integer, ForeignKey("Promociones.id_promotions"))
    employee_id = Column(Integer, ForeignKey("Empleado.employee_id"))

    client = relationship("Cliente", back_populates="reservas")
    funcion = relationship("Funcion")  # Ahora funcion se enlaza bien
    promocion = relationship("Promociones")
    empleado = relationship("Empleado")
    reserva_asientos = relationship("Reserva_asientos", back_populates="reserva")


class Funcion(Base):
    __tablename__ = "Funcion"
    id_funcion = Column(Integer, primary_key=True, index=True)
    id_pelicula = Column(Integer, ForeignKey("Pelicula.id_pelicula"))
    employee_id = Column(Integer, ForeignKey("Empleado.employee_id"))
    Schedule = Column(DateTime)

    pelicula = relationship("Pelicula")
    empleado = relationship("Empleado")
    

class Reserva_asientos(Base):
    __tablename__ = "Reserva_asientos"
    reservationseat_id = Column(String(80), primary_key=True)
    reservation_id = Column(Integer, ForeignKey("Reserva.reservation_id"))
    ids_seats = Column(String(50), ForeignKey("Asiento.ids_seats"))

    reserva = relationship("Reserva")
    asiento = relationship("Asiento")

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
