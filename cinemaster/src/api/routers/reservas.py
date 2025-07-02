from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, Union

from models.database import get_db, Reserva_asientos, HorarioAsientos
from controllers.receipt_controller import ReceiptController
from commands.reserve_seat_command import ReserveSeatCommand
from services.email_observer import EmailSenderObserver

router = APIRouter(prefix="/reservas", tags=["Reservas"])

# Modelo Pydantic con ejemplo realista
class ReservaRequest(BaseModel):
    client_id: int = Field(..., example=5, description="ID del cliente en el sistema")
    id_funcion: int = Field(..., example=1, description="ID de la función/horario seleccionado")
    seat_id: str = Field(..., example="A5", description="Identificador del asiento seleccionado")
    movie_name: str = Field(..., example="Bajoterra", description="Nombre de la película")
    showtime_string: str = Field(..., example="2025-05-30 23:00", description="Horario de la función")
    imagen: Optional[str] = Field(None, example="/path/to/bajoterra.jpg", description="Ruta de la imagen de la película")
    cliente_nombre: str = Field(..., example="Seba", description="Nombre completo del cliente")
    costo_entrada: float = Field(..., example=12.0, description="Precio de la entrada")
    metodo_pago: str = Field(..., example="tarjeta", description="Método de pago utilizado")
    cliente_email: Optional[str] = Field(None, example="spereda2024@alu.uct.cl", description="Email del cliente para confirmación")

class ReservaResponse(BaseModel):
    success: bool = Field(..., example=True, description="Indica si la reserva fue exitosa")
    message: str = Field(..., example="Reserva confirmada exitosamente. Boleta generada y email enviado.", description="Mensaje descriptivo del resultado")
    reserva_id: Optional[Union[int, str]] = Field(None, example="b058dd05-7b18-4edb-8713-e77cb3897a7a", description="ID de la reserva creada (puede ser entero o UUID)")

def asiento_disponible_para_funcion(seat_id: str, id_funcion: int, db: Session) -> bool:
    """Verifica si un asiento está disponible para una función específica"""
    horario_asiento = db.query(HorarioAsientos).filter(
        HorarioAsientos.asiento_id == seat_id,
        HorarioAsientos.horario_id == id_funcion,
        HorarioAsientos.Available == 1
    ).first()
    return horario_asiento is not None

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

        # 2. Crear la reserva en la base de datos
        reserve_command = ReserveSeatCommand(
            reserva.client_id, 
            reserva.id_funcion, 
            reserva.seat_id, 
            db
        )
        reserva_creada = reserve_command.execute()

        # 3. Generar boleta PDF
        receipt_controller = ReceiptController()
        receipt_controller.generar_boleta(
            reserva.movie_name, 
            reserva.showtime_string, 
            reserva.seat_id, 
            reserva.imagen, 
            reserva.cliente_nombre
        )
        receipt_controller.confirmar_boleta()

        # 4. Enviar email de confirmación
        if reserva.cliente_email:
            email_sender = EmailSenderObserver()
            email_sender.send_email(
                reserva.cliente_email, 
                reserva.cliente_nombre, 
                reserva.movie_name, 
                "Gracias por su compra. Adjuntamos su boleta."
            )
            print(f"📤 Correo enviado a {reserva.cliente_email}")

        return ReservaResponse(
            success=True,
            message="Reserva confirmada exitosamente. Boleta generada y email enviado.",
            reserva_id=str(reserva_creada.reservationseat_id)  # Convertir a string para consistencia
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")