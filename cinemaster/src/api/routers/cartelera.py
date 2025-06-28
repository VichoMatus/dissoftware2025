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