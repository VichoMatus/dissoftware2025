from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Union

from api.database import get_db
from api.schemas.reserva_schemas import ReservaRequest, ReservaResponse
from api.commands import CommandInvoker, ReserveSeatCommand, GenerateReceiptCommand, NotificationCommand
from api.observers import EmailObserver, ReservationSubject

router = APIRouter(prefix="/reservas", tags=["Reservas"])

# Crear sujeto de reserva y observador de email (instancias globales)
reservation_subject = ReservationSubject()
email_observer = EmailObserver()

# Registrar el observador de email
reservation_subject.attach(email_observer)

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
    Confirma una reserva completa usando el patrón Command + Observer.
    
    ✅ Verifica disponibilidad del asiento
    ✅ Ejecuta comando de reserva
    ✅ Ejecuta comando de generación de boleta
    ✅ Ejecuta comando de notificación (envío de email automático)
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

        # 3. Crear y ejecutar comando de generación de boleta usando patrón Builder
        receipt_command = GenerateReceiptCommand(
            movie_name=reserva.movie_name,
            showtime=reserva.showtime_string,
            seat=reserva.seat_id,
            client_name=reserva.cliente_nombre,
            imagen=reserva.imagen,
            ticket_price=reserva.costo_entrada  # Incluir el precio del boleto
        )
        
        boleta_resultado = invoker.execute_single_command(receipt_command)
        
        if boleta_resultado.get("success"):
            print(f"✅ Boleta generada: {boleta_resultado.get('filename')}")
        else:
            print(f"❌ Error generando boleta: {boleta_resultado.get('message')}")

        # 4. Crear y ejecutar comando de notificación (envío automático de email)
        if reserva.cliente_email:
            event_data = {
                "cliente_email": reserva.cliente_email,
                "cliente_nombre": reserva.cliente_nombre,
                "movie_name": reserva.movie_name,
                "seat_id": reserva.seat_id,
                "showtime_string": reserva.showtime_string,
                "pdf_path": boleta_resultado.get("pdf_path"),
                "reserva_id": reserva_resultado.get("reserva_seat_id"),
                "reservation_id": reserva_resultado.get("reservation_id")
            }
            
            notification_command = NotificationCommand(
                reservation_subject=reservation_subject,
                event_data=event_data
            )
            
            notification_resultado = invoker.execute_single_command(notification_command)
            
            if notification_resultado.get("success"):
                print(f"✅ Notificaciones enviadas: {notification_resultado.get('message')}")
            else:
                print(f"❌ Error enviando notificaciones: {notification_resultado.get('message')}")

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