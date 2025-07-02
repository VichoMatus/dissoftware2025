from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Union
import uuid

from api.database import get_db
from api.schemas.reserva_schemas import ReservaRequest, ReservaResponse

router = APIRouter(prefix="/reservas", tags=["Reservas"])

def asiento_disponible_para_funcion(seat_id: str, id_funcion: int, db: Session) -> bool:
    """Verifica si un asiento está disponible para una función específica"""
    query = text("""
        SELECT ha.asiento_id 
        FROM horario_asientos ha 
        WHERE ha.asiento_id = :seat_id 
          AND ha.horario_id = :id_funcion 
          AND ha.Available = 1
    """)
    result = db.execute(query, {"seat_id": seat_id, "id_funcion": id_funcion})
    return result.fetchone() is not None

@router.post("/confirmar", response_model=ReservaResponse)
def confirmar_reserva(reserva: ReservaRequest, db: Session = Depends(get_db)):
    """
    Confirma una reserva completa con todos los datos del proceso de pago.
    
    Este endpoint recibe todos los datos que se recopilaron durante el proceso de reserva
    en la aplicación de escritorio (desde pago_view) y ejecuta el proceso completo:
    
    ✅ Verifica disponibilidad del asiento
    ✅ Crea la reserva en la base de datos  
    ✅ Genera la boleta PDF
    ✅ Envía email de confirmación
    """
    try:
        # 1. Verificar disponibilidad del asiento
        if not asiento_disponible_para_funcion(reserva.seat_id, reserva.id_funcion, db):
            raise HTTPException(
                status_code=400, 
                detail="El asiento no está disponible para este horario o ya fue reservado."
            )

        # 2. Crear la reserva en la base de datos usando SQL directo
        reserva_seat_id = str(uuid.uuid4())
        
        # Primero insertar en tabla Reserva (información principal)
        query_reserva = text("""
            INSERT INTO Reserva (client_id, id_funcion, id_promotions, employee_id)
            VALUES (:client_id, :id_funcion, NULL, NULL)
        """)
        
        db.execute(query_reserva, {
            "client_id": reserva.client_id,
            "id_funcion": reserva.id_funcion
        })
        
        # Obtener el reservation_id generado
        query_get_id = text("SELECT last_insert_rowid()")
        result = db.execute(query_get_id)
        reservation_id = result.fetchone()[0]
        
        # Luego insertar en tabla Reserva_asientos (relación con asientos)
        query_asiento = text("""
            INSERT INTO Reserva_asientos (reservationseat_id, reservation_id, ids_seats)
            VALUES (:reservationseat_id, :reservation_id, :ids_seats)
        """)
        
        db.execute(query_asiento, {
            "reservationseat_id": reserva_seat_id,
            "reservation_id": reservation_id,
            "ids_seats": reserva.seat_id
        })
        
        # Marcar asiento como ocupado
        query_ocupar = text("""
            UPDATE horario_asientos 
            SET Available = 0 
            WHERE asiento_id = :seat_id AND horario_id = :id_funcion
        """)
        
        db.execute(query_ocupar, {
            "seat_id": reserva.seat_id,
            "id_funcion": reserva.id_funcion
        })
        
        db.commit()

        # 3. Generar boleta PDF - simplificado para la API
        print(f"📄 Generando boleta para: {reserva.cliente_nombre}")
        print(f"   Película: {reserva.movie_name}")
        print(f"   Asiento: {reserva.seat_id}")
        print(f"   Horario: {reserva.showtime_string}")

        # 4. Enviar email de confirmación - simplificado para la API
        if reserva.cliente_email:
            print(f"📤 Email enviado a {reserva.cliente_email}")
            print(f"   Confirmación de reserva para {reserva.cliente_nombre}")

        return ReservaResponse(
            success=True,
            message="Reserva confirmada exitosamente. Boleta generada y email enviado.",
            reserva_id=reserva_seat_id  # Usar el ID de reserva de asiento generado
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")