from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from api.schemas.empleado_schemas import (
    EmpleadoCreate, 
    EmpleadoUpdate, 
    EmpleadoResponse, 
    EmpleadoCloneRequest
)
from api.database import get_db

router = APIRouter()

@router.post("/empleados/", response_model=EmpleadoResponse)
def crear_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO Empleado (Name, Email, Password)
        VALUES (:name, :email, :password)
    """)
    
    result = db.execute(query, {
        "name": empleado.Name,
        "email": empleado.Email,
        "password": empleado.Password
    })
    db.commit()
    
    empleado_id = result.lastrowid
    return obtener_empleado(empleado_id, db)

@router.get("/empleados/", response_model=List[EmpleadoResponse])
def obtener_empleados(db: Session = Depends(get_db)):
    query = text("SELECT employee_id, Name, Email FROM Empleado")
    result = db.execute(query)
    empleados = []
    for row in result:
        empleados.append(EmpleadoResponse(
            employee_id=row.employee_id,
            Name=row.Name,
            Email=row.Email
        ))
    return empleados

@router.get("/empleados/{empleado_id}", response_model=EmpleadoResponse)
def obtener_empleado(empleado_id: int, db: Session = Depends(get_db)):
    query = text("SELECT employee_id, Name, Email FROM Empleado WHERE employee_id = :id")
    result = db.execute(query, {"id": empleado_id})
    row = result.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return EmpleadoResponse(
        employee_id=row.employee_id,
        Name=row.Name,
        Email=row.Email
    )

@router.put("/empleados/{empleado_id}", response_model=EmpleadoResponse)
def actualizar_empleado(empleado_id: int, empleado_update: EmpleadoUpdate, db: Session = Depends(get_db)):
    # Verificar que el empleado existe
    empleado_existente = obtener_empleado(empleado_id, db)
    
    # Preparar datos para actualizar
    update_data = empleado_update.dict(exclude_unset=True)
    if not update_data:
        return empleado_existente
    
    # Construir query dinámicamente
    set_clauses = []
    params = {"id": empleado_id}
    
    if "Name" in update_data:
        set_clauses.append("Name = :name")
        params["name"] = update_data["Name"]
    if "Email" in update_data:
        set_clauses.append("Email = :email")
        params["email"] = update_data["Email"]
    if "Password" in update_data:
        set_clauses.append("Password = :password")
        params["password"] = update_data["Password"]
    
    query = text(f"UPDATE Empleado SET {', '.join(set_clauses)} WHERE employee_id = :id")
    db.execute(query, params)
    db.commit()
    
    return obtener_empleado(empleado_id, db)

@router.delete("/empleados/{empleado_id}")
def eliminar_empleado(empleado_id: int, db: Session = Depends(get_db)):
    # Verificar que existe
    obtener_empleado(empleado_id, db)
    
    query = text("DELETE FROM Empleado WHERE employee_id = :id")
    db.execute(query, {"id": empleado_id})
    db.commit()
    return {"message": "Empleado eliminado exitosamente"}

@router.post("/empleados/{empleado_id}/clone", response_model=EmpleadoResponse)
def clonar_empleado(empleado_id: int, datos_clone: EmpleadoCloneRequest, db: Session = Depends(get_db)):
    """
    Clona un empleado existente usando el patrón Prototype.
    Requiere nuevos datos (nombre, email, password) para el empleado clonado.
    La lógica de clonado se implementa en la API usando solo esquemas.
    """
    # Verificar que el empleado original existe
    query_original = text("SELECT employee_id FROM Empleado WHERE employee_id = :id")
    result = db.execute(query_original, {"id": empleado_id})
    if result.fetchone() is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    # Verificar que el email no exista ya
    query_email = text("SELECT employee_id FROM Empleado WHERE Email = :email")
    result_email = db.execute(query_email, {"email": datos_clone.Email})
    if result_email.fetchone():
        raise HTTPException(status_code=400, detail="Ya existe un empleado con ese email")
    
    # Implementar patrón Prototype: crear nuevo empleado basado en el original
    query_clone = text("""
        INSERT INTO Empleado (Name, Email, Password)
        VALUES (:name, :email, :password)
    """)
    
    result = db.execute(query_clone, {
        "name": datos_clone.Name,
        "email": datos_clone.Email,
        "password": datos_clone.Password
    })
    db.commit()
    
    # Retornar empleado clonado
    nuevo_empleado_id = result.lastrowid
    return obtener_empleado(nuevo_empleado_id, db)
