from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from services.Tfuncion_service import FuncionService

router = APIRouter(prefix="/funciones", tags=["Funciones"])

@router.get("/")
def listar_funciones(db: Session = Depends(get_db)):
    return FuncionService.listar_funciones(db)

@router.post("/")
def crear_funcion(id_pelicula: int, employee_id: int, Schedule: str, db: Session = Depends(get_db)):
    return FuncionService.crear_funcion(db, id_pelicula, employee_id, Schedule)

@router.put("/{id_funcion}")
def actualizar_funcion(id_funcion: int, id_pelicula: int, employee_id: int, Schedule: str, db: Session = Depends(get_db)):
    return FuncionService.actualizar_funcion(db, id_funcion, id_pelicula, employee_id, Schedule)

@router.delete("/{id_funcion}")
def eliminar_funcion(id_funcion: int, db: Session = Depends(get_db)):
    return FuncionService.eliminar_funcion(db, id_funcion)