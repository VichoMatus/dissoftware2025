from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from services.Tpromociones_services import PromocionesService

router = APIRouter(prefix="/promociones", tags=["Promociones"])

@router.get("/")
def listar_promociones(db: Session = Depends(get_db)):
    return PromocionesService.listar_promociones(db)

@router.post("/")
def crear_promocion(Type: str, Membership: int, db: Session = Depends(get_db)):
    return PromocionesService.crear_promocion(db, Type, Membership)

@router.put("/{id_promotions}")
def actualizar_promocion(id_promotions: int, Type: str, Membership: int, db: Session = Depends(get_db)):
    return PromocionesService.actualizar_promocion(db, id_promotions, Type, Membership)

@router.delete("/{id_promotions}")
def eliminar_promocion(id_promotions: int, db: Session = Depends(get_db)):
    return PromocionesService.eliminar_promocion(db, id_promotions)