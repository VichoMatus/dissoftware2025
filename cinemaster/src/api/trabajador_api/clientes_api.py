from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from services.Tcliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/")
def listar_clientes(db: Session = Depends(get_db)):
    return ClienteService.listar_clientes(db)

@router.post("/")
def crear_cliente(nombre: str, email: str, password: str, db: Session = Depends(get_db)):
    return ClienteService.crear_cliente(db, nombre, email, password)

@router.put("/{cliente_id}")
def actualizar_cliente(cliente_id: int, nombre: str, email: str, password: str, db: Session = Depends(get_db)):
    return ClienteService.actualizar_cliente(db, cliente_id, nombre, email, password)

@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return ClienteService.eliminar_cliente(db, cliente_id)