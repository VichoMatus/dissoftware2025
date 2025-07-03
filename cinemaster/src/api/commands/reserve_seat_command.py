from .command import Command
from sqlalchemy.orm import Session
from sqlalchemy import text
import uuid
from typing import Dict, Any

class ReserveSeatCommand(Command):
    """
    Comando para reservar un asiento en la API.
    Solo se encarga de la lógica de base de datos, sin notificaciones.
    """
    
    def __init__(self, client_id: int, id_funcion: int, seat_id: str, db: Session):
        self.client_id = client_id
        self.id_funcion = id_funcion
        self.seat_id = seat_id
        self.db = db
        self.reserva_seat_id = None
        self.reservation_id = None
    
    def execute(self) -> Dict[str, Any]:
        """
        Ejecuta el proceso completo de reserva:
        1. Inserta en tabla Reserva
        2. Obtiene el ID generado
        3. Inserta en tabla Reserva_asientos
        4. Marca el asiento como ocupado
        5. Hace commit de la transacción
        
        Returns:
            Dict con información de la reserva creada
        """
        try:
            # Generar UUID para la reserva de asiento
            self.reserva_seat_id = str(uuid.uuid4())
            
            # 1. Insertar en tabla Reserva (información principal)
            query_reserva = text("""
                INSERT INTO Reserva (client_id, id_funcion, id_promotions, employee_id)
                VALUES (:client_id, :id_funcion, NULL, NULL)
            """)
            
            self.db.execute(query_reserva, {
                "client_id": self.client_id,
                "id_funcion": self.id_funcion
            })
            
            # 2. Obtener el reservation_id generado
            query_get_id = text("SELECT last_insert_rowid()")
            result = self.db.execute(query_get_id)
            self.reservation_id = result.fetchone()[0]
            
            # 3. Insertar en tabla Reserva_asientos (relación con asientos)
            query_asiento = text("""
                INSERT INTO Reserva_asientos (reservationseat_id, reservation_id, ids_seats)
                VALUES (:reservationseat_id, :reservation_id, :ids_seats)
            """)
            
            self.db.execute(query_asiento, {
                "reservationseat_id": self.reserva_seat_id,
                "reservation_id": self.reservation_id,
                "ids_seats": self.seat_id
            })
            
            # 4. Marcar asiento como ocupado
            query_ocupar = text("""
                UPDATE horario_asientos 
                SET Available = 0 
                WHERE asiento_id = :seat_id AND horario_id = :id_funcion
            """)
            
            self.db.execute(query_ocupar, {
                "seat_id": self.seat_id,
                "id_funcion": self.id_funcion
            })
            
            # 5. Confirmar transacción
            self.db.commit()
            
            print(f"✅ Reserva creada: ID={self.reservation_id}, Asiento={self.seat_id}")
            
            return {
                "success": True,
                "reserva_seat_id": self.reserva_seat_id,
                "reservation_id": self.reservation_id,
                "client_id": self.client_id,
                "seat_id": self.seat_id,
                "id_funcion": self.id_funcion
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error en ReserveSeatCommand: {e}")
            return {
                "success": False,
                "error": str(e),
                "reserva_seat_id": None,
                "reservation_id": None
            }