from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from services.Treservas_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.get("/")
def listar_reservas(db: Session = Depends(get_db)):
    return ReservaService.listar_reservas(db)

@router.post("/")
def crear_reserva(client_id: int, id_funcion: int, id_promotions: int, employee_id: int, db: Session = Depends(get_db)):
    return ReservaService.crear_reserva(db, client_id, id_funcion, id_promotions, employee_id)

@router.put("/{reservation_id}")
def actualizar_reserva(reservation_id: int, client_id: int, id_funcion: int, id_promotions: int, employee_id: int, db: Session = Depends(get_db)):
    return ReservaService.actualizar_reserva(db, reservation_id, client_id, id_funcion, id_promotions, employee_id)

@router.delete("/{reservation_id}")
def eliminar_reserva(reservation_id: int, db: Session = Depends(get_db)):
    return ReservaService.eliminar_reserva(db, reservation_id)