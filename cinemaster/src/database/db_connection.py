from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models.database import Reserva, Cliente, Funcion, Pelicula, Reserva_asientos, Asiento
import threading

class DatabaseConnection:
    """
    Patrón Singleton para garantizar una única conexión a la base de datos.
    Thread-safe para aplicaciones multi-threading.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Doble verificación para thread-safety
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.DATABASE_URL = "sqlite:///./test.db"
        self.engine = create_engine(
            self.DATABASE_URL, 
            connect_args={"check_same_thread": False}
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )
        self._initialized = True
    
    def get_session(self):
        """Retorna una nueva sesión de base de datos"""
        return self.SessionLocal()
    
    def get_engine(self):
        """Retorna el engine de SQLAlchemy"""
        return self.engine

# Instancia global del singleton
db_singleton = DatabaseConnection()

# Mantener compatibilidad con el código existente
SessionLocal = db_singleton.SessionLocal
engine = db_singleton.engine

def get_db():
    """
    Función generadora que proporciona una sesión de base de datos
    usando el patrón Singleton para la conexión.
    """
    db = db_singleton.get_session()
    try:
        yield db
    finally:
        db.close()

def get_reservation_details(reservation_id):
    """
    Obtiene los detalles de una reserva específica usando el singleton
    para la conexión a la base de datos.
    """
    db = db_singleton.get_session()
    try:
        reserva = (
            db.query(Reserva)
            .filter(Reserva.reservation_id == reservation_id)
            .options(
                joinedload(Reserva.client),
                joinedload(Reserva.funcion),
                joinedload(Reserva.reserva_asientos).joinedload(Reserva_asientos.asiento)
            )
            .first()
        )
        if not reserva:
            return None

        cliente = reserva.client
        funcion = reserva.funcion
        asiento = reserva.reserva_asientos[0].asiento if reserva.reserva_asientos else None
        pelicula = db.query(Pelicula).filter(Pelicula.id_pelicula == funcion.id_pelicula).first() if funcion else None

        details = {
            "movie_name": pelicula.Title if pelicula else "N/A",
            "showtime_string": funcion.Schedule.strftime("%Y-%m-%d %H:%M") if funcion else "N/A",
            "seat": asiento.ids_seats if asiento else "N/A",
            "cliente_nombre": cliente.nombre if cliente else "N/A",
            "price": 12.0
        }
        return details
    finally:
        db.close()

def get_database_instance():
    """
    Función de conveniencia para obtener la instancia singleton
    de la conexión a la base de datos.
    """
    return db_singleton

def close_all_connections():
    """
    Cierra todas las conexiones activas.
    Útil para limpieza al finalizar la aplicación.
    """
    if hasattr(db_singleton, 'engine'):
        db_singleton.engine.dispose()

def test_connection():
    """
    Prueba la conexión a la base de datos.
    Retorna True si la conexión es exitosa, False en caso contrario.
    """
    try:
        db = db_singleton.get_session()
        # Realizar una consulta simple para probar la conexión
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"Error en la conexión a la base de datos: {e}")
        return False
