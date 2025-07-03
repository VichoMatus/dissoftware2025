from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from services.Tcliente_service import ClienteService
from api.schemas.cliente_schemas import ClienteCreate

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/")
def listar_clientes(db: Session = Depends(get_db)):
    return ClienteService.listar_clientes(db)

@router.post("/")
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteService.crear_cliente(db, cliente.nombre, cliente.Email, cliente.Password)

@router.put("/{cliente_id}")
def actualizar_cliente(cliente_id: int, cliente: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteService.actualizar_cliente(db, cliente_id, cliente.nombre, cliente.Email, cliente.Password)

@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return ClienteService.eliminar_cliente(db, cliente_id)