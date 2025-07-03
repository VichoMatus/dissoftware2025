from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from models.database import SessionLocal, Empleado, Cliente

# --- Modelos Pydantic para validación y serialización ---

# Modelos para Empleados
class EmployeeBase(BaseModel):
    Name: str
    Email: EmailStr

class EmployeeCreate(EmployeeBase):
    Password: str

class EmployeeUpdate(EmployeeBase):
    Password: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    employee_id: int

    class Config:
        orm_mode = True

# Modelos para Clientes
class ClientBase(BaseModel):
    nombre: str
    Email: EmailStr
    Membership: bool = False

class ClientCreate(ClientBase):
    Password: str

class ClientUpdate(ClientBase):
    Password: Optional[str] = None

class ClientResponse(ClientBase):
    cliente_id: int

    class Config:
        orm_mode = True

# --- Router de FastAPI ---
router = APIRouter(
    prefix="/admin",
    tags=["Admin Management"]
)

# --- Dependencia para la sesión de la base de datos ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================ ENDPOINTS DE EMPLEADOS ============================

@router.get("/employees/", response_model=List[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    employees = db.query(Empleado).all()
    return employees

@router.post("/employees/", response_model=EmployeeResponse, status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # Aquí deberías hashear la contraseña antes de guardarla
    db_employee = Empleado(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee_data: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = db.query(Empleado).filter(Empleado.employee_id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    update_data = employee_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
        
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(Empleado).filter(Empleado.employee_id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    db.delete(db_employee)
    db.commit()
    return {"ok": True} # No se envía contenido en un 204

# ============================ ENDPOINTS DE CLIENTES ============================

@router.get("/clients/", response_model=List[ClientResponse])
def get_all_clients(db: Session = Depends(get_db)):
    clients = db.query(Cliente).all()
    return clients

@router.post("/clients/", response_model=ClientResponse, status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Cliente(**client.dict(), Reservation_history="")
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.put("/clients/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_data: ClientUpdate, db: Session = Depends(get_db)):
    db_client = db.query(Cliente).filter(Cliente.cliente_id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    update_data = client_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_client, key, value)
        
    db.commit()
    db.refresh(db_client)
    return db_client

@router.delete("/clients/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Cliente).filter(Cliente.cliente_id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_client)
    db.commit()
    return {"ok": True}

@router.post("/clients/clone/{client_id}", response_model=ClientResponse)
def clone_client(client_id: int, db: Session = Depends(get_db)):
    original_client = db.query(Cliente).filter(Cliente.cliente_id == client_id).first()
    if not original_client:
        raise HTTPException(status_code=404, detail="Cliente a clonar no encontrado")
    
    cloned_client = original_client.clone() # Usamos el método clone que ya tenías
    # No guardamos el clon, solo devolvemos sus datos para el formulario
    return ClientResponse.from_orm(cloned_client)