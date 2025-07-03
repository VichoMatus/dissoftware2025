from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.funcion_schemas import FuncionCreate
from models.database import get_db
from services.Tfuncion_service import FuncionService

router = APIRouter(prefix="/funciones", tags=["Funciones"])

@router.get("/")
def listar_funciones(db: Session = Depends(get_db)):
    return FuncionService.listar_funciones(db)

@router.post("/")
def crear_funcion(funcion: FuncionCreate, db: Session = Depends(get_db)):
    return FuncionService.crear_funcion(db, funcion.id_pelicula, funcion.employee_id, funcion.Schedule)

@router.put("/{id_funcion}")
def actualizar_funcion(id_funcion: int, funcion: FuncionCreate, db: Session = Depends(get_db)):
    return FuncionService.actualizar_funcion(db, id_funcion, funcion.id_pelicula, funcion.employee_id, funcion.Schedule)

@router.delete("/{id_funcion}")
def eliminar_funcion(id_funcion: int, db: Session = Depends(get_db)):
    return FuncionService.eliminar_funcion(db, id_funcion)