from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.cliente_schemas import ClienteCreate  # importa el modelo
from models.database import get_db, Cliente

router = APIRouter()

@router.post("/clientes/")
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    nuevo = Cliente(
        nombre=cliente.nombre,
        Email=cliente.Email,
        Password=cliente.Password,
        Membership=False,
        Reservation_history=""
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo