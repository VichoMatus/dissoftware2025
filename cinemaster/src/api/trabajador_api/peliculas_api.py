from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from services.Tpelicula_service import PeliculaService

router = APIRouter(prefix="/peliculas", tags=["Películas"])

@router.get("/")
def listar_peliculas(db: Session = Depends(get_db)):
    return PeliculaService.listar_peliculas(db)

@router.post("/")
def crear_pelicula(Title: str, Duration: int, Gender: str, Image_path: str, db: Session = Depends(get_db)):
    return PeliculaService.crear_pelicula(db, Title, Duration, Gender, Image_path)

@router.put("/{id_pelicula}")
def actualizar_pelicula(id_pelicula: int, Title: str, Duration: int, Gender: str, Image_path: str, db: Session = Depends(get_db)):
    return PeliculaService.actualizar_pelicula(db, id_pelicula, Title, Duration, Gender, Image_path)

@router.delete("/{id_pelicula}")
def eliminar_pelicula(id_pelicula: int, db: Session = Depends(get_db)):
    return PeliculaService.eliminar_pelicula(db, id_pelicula)