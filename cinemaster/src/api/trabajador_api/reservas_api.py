from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.reserva_schemas import ReservaCreate
from models.database import get_db
from services.Treservas_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.get("/")
def listar_reservas(db: Session = Depends(get_db)):
    return ReservaService.listar_reservas(db)

@router.post("/")
def crear_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    return ReservaService.crear_reserva(
        db,
        client_id=reserva.client_id,
        id_funcion=reserva.id_funcion,
        employee_id=reserva.employee_id
    )

@router.put("/{reservation_id}")
def actualizar_reserva(reservation_id: int, reserva: ReservaCreate, db: Session = Depends(get_db)):
    return ReservaService.actualizar_reserva(
        db,
        reservation_id=reservation_id,
        client_id=reserva.client_id,
        id_funcion=reserva.id_funcion,
        employee_id=reserva.employee_id
    )

@router.delete("/{reservation_id}")
def eliminar_reserva(reservation_id: int, db: Session = Depends(get_db)):
    return ReservaService.eliminar_reserva(db, reservation_id)