from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from api.services.cartelera_service import CarteleraService

router = APIRouter(prefix="/cartelera", tags=["Cartelera"])

@router.get("/")
def listar_cartelera(db: Session = Depends(get_db)):
    """
    Devuelve la lista de todas las películas en cartelera con todos sus datos.
    """
    return CarteleraService.listar_peliculas(db)


@router.get("/{pelicula_id}/horarios")
def obtener_horarios_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    """Obtiene los horarios de una película específica"""
    return CarteleraService.obtener_horarios(db, pelicula_id)


@router.get("/horarios/{horario_id}/asientos")
def obtener_asientos_disponibles(horario_id: int, db: Session = Depends(get_db)):
    """Obtiene los asientos disponibles para un horario específico"""
    return CarteleraService.obtener_asientos_disponibles(db, horario_id)