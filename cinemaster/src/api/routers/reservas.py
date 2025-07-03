from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import get_db
from api.schemas.reserva_schemas import ReservaRequest, ReservaResponse
from api.facades import booking_facade

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.post("/confirmar", response_model=ReservaResponse)
def confirmar_reserva(reserva: ReservaRequest, db: Session = Depends(get_db)):
    """
    Confirma una reserva completa usando el patrón Facade.
    Simplifica toda la lógica que antes estaba aquí.
    """
    try:
        # Convertir datos para el facade
        reservation_data = {
            "client_id": reserva.client_id,
            "id_funcion": reserva.id_funcion,
            "seat_id": reserva.seat_id,
            "movie_name": reserva.movie_name,
            "showtime_string": reserva.showtime_string,
            "imagen": reserva.imagen,
            "cliente_nombre": reserva.cliente_nombre,
            "cliente_email": reserva.cliente_email,
            "costo_entrada": reserva.costo_entrada
        }
        
        # Usar el facade (toda la lógica encapsulada)
        resultado = booking_facade.book_complete_reservation(reservation_data, db)
        
        if resultado["success"]:
            return ReservaResponse(
                success=True,
                message=resultado["message"],
                reserva_id=resultado["reserva_id"]
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=resultado["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en confirmar_reserva: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")