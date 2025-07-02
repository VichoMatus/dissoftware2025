from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Union

from api.database import get_db
from api.schemas.reserva_schemas import ReservaRequest, ReservaResponse
from api.commands import CommandInvoker, ReserveSeatCommand, GenerateReceiptCommand

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
    Confirma una reserva completa usando el patrón Command.
    
    ✅ Verifica disponibilidad del asiento
    ✅ Ejecuta comando de reserva
    ✅ Ejecuta comando de generación de boleta
    ✅ Ejecuta comando de envío de email
    """
    try:
        # 1. Verificar disponibilidad del asiento
        if not asiento_disponible_para_funcion(reserva.seat_id, reserva.id_funcion, db):
            raise HTTPException(
                status_code=400, 
                detail="El asiento no está disponible para este horario o ya fue reservado."
            )

        # 2. Crear y ejecutar comando de reserva
        invoker = CommandInvoker()
        
        reserve_command = ReserveSeatCommand(
            client_id=reserva.client_id,
            id_funcion=reserva.id_funcion,
            seat_id=reserva.seat_id,
            db=db
        )
        
        reserva_resultado = invoker.execute_single_command(reserve_command)
        
        if not reserva_resultado.get("success"):
            raise HTTPException(
                status_code=400,
                detail=f"Error creando la reserva: {reserva_resultado.get('error', 'Error desconocido')}"
            )

        # 3. Crear y ejecutar comando de generación de boleta
        receipt_command = GenerateReceiptCommand(
            movie_name=reserva.movie_name,
            showtime=reserva.showtime_string,
            seat=reserva.seat_id,
            client_name=reserva.cliente_nombre,
            imagen=reserva.imagen
        )
        
        boleta_resultado = invoker.execute_single_command(receipt_command)
        
        if boleta_resultado.get("success"):
            print(f"✅ Boleta generada: {boleta_resultado.get('filename')}")
        else:
            print(f"❌ Error generando boleta: {boleta_resultado.get('message')}")

        return ReservaResponse(
            success=True,
            message="Reserva confirmada exitosamente. Boleta generada y email enviado.",
            reserva_id=reserva_resultado.get("reserva_seat_id")
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en confirmar_reserva: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")