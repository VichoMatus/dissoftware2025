from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from api.schemas.cliente_schemas import (
    ClienteCreate, 
    ClienteUpdate, 
    ClienteResponse, 
    ClienteCloneRequest
)
from api.database import get_db

router = APIRouter()

@router.post("/clientes/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    # Insertar usando SQL directo y esquemas
    query = text("""
        INSERT INTO Cliente (nombre, Email, Password, Membership, Reservation_history)
        VALUES (:nombre, :email, :password, :membership, :history)
    """)
    
    result = db.execute(query, {
        "nombre": cliente.nombre,
        "email": cliente.Email,
        "password": cliente.Password,
        "membership": False,
        "history": ""
    })
    db.commit()
    
    # Obtener el cliente creado
    cliente_id = result.lastrowid
    return obtener_cliente(cliente_id, db)

@router.get("/clientes/", response_model=List[ClienteResponse])
def obtener_clientes(db: Session = Depends(get_db)):
    query = text("SELECT cliente_id, nombre, Email, Membership FROM Cliente")
    result = db.execute(query)
    clientes = []
    for row in result:
        clientes.append(ClienteResponse(
            cliente_id=row.cliente_id,
            nombre=row.nombre,
            Email=row.Email,
            Membership=bool(row.Membership)
        ))
    return clientes

@router.get("/clientes/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    query = text("SELECT cliente_id, nombre, Email, Membership FROM Cliente WHERE cliente_id = :id")
    result = db.execute(query, {"id": cliente_id})
    row = result.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return ClienteResponse(
        cliente_id=row.cliente_id,
        nombre=row.nombre,
        Email=row.Email,
        Membership=bool(row.Membership)
    )

@router.put("/clientes/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente_update: ClienteUpdate, db: Session = Depends(get_db)):
    # Verificar que el cliente existe
    cliente_existente = obtener_cliente(cliente_id, db)
    
    # Preparar datos para actualizar
    update_data = cliente_update.dict(exclude_unset=True)
    if not update_data:
        return cliente_existente
    
    # Construir query dinámicamente
    set_clauses = []
    params = {"id": cliente_id}
    
    if "nombre" in update_data:
        set_clauses.append("nombre = :nombre")
        params["nombre"] = update_data["nombre"]
    if "Email" in update_data:
        set_clauses.append("Email = :email")
        params["email"] = update_data["Email"]
    if "Password" in update_data:
        set_clauses.append("Password = :password")
        params["password"] = update_data["Password"]
    
    query = text(f"UPDATE Cliente SET {', '.join(set_clauses)} WHERE cliente_id = :id")
    db.execute(query, params)
    db.commit()
    
    return obtener_cliente(cliente_id, db)

@router.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    # Verificar que existe
    obtener_cliente(cliente_id, db)
    
    query = text("DELETE FROM Cliente WHERE cliente_id = :id")
    db.execute(query, {"id": cliente_id})
    db.commit()
    return {"message": "Cliente eliminado exitosamente"}

@router.post("/clientes/{cliente_id}/clone", response_model=ClienteResponse)
def clonar_cliente(cliente_id: int, datos_clone: ClienteCloneRequest, db: Session = Depends(get_db)):
    """
    Clona un cliente existente usando el patrón Prototype.
    Requiere nuevos datos (nombre, email, password) para el cliente clonado.
    La lógica de clonado se implementa en la API usando solo esquemas.
    """
    try:
        print(f"DEBUG: Intentando clonar cliente {cliente_id}")
        print(f"DEBUG: Datos de clonado: {datos_clone}")
        
        # Obtener cliente original
        query_original = text("SELECT cliente_id, nombre, Email, Membership FROM Cliente WHERE cliente_id = :id")
        result = db.execute(query_original, {"id": cliente_id})
        cliente_original = result.fetchone()
        print(f"DEBUG: Cliente original encontrado: {cliente_original}")
        
        if cliente_original is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Verificar que el email no exista ya
        query_email = text("SELECT cliente_id FROM Cliente WHERE Email = :email")
        result_email = db.execute(query_email, {"email": datos_clone.Email})
        cliente_existente = result_email.fetchone()
        print(f"DEBUG: Cliente con email existente: {cliente_existente}")
        
        if cliente_existente:
            print(f"DEBUG: Email ya existe, retornando error 400")
            raise HTTPException(status_code=400, detail="Ya existe un cliente con ese email")
        
        # Implementar patrón Prototype: crear nuevo cliente basado en el original
        query_clone = text("""
            INSERT INTO Cliente (nombre, Email, Password, Membership, Reservation_history)
            VALUES (:nombre, :email, :password, :membership, :history)
        """)
        
        params = {
            "nombre": datos_clone.nombre,
            "email": datos_clone.Email,
            "password": datos_clone.Password,
            # Copiar atributos del cliente original (patrón Prototype)
            "membership": cliente_original.Membership,
            "history": ""  # Resetear historial para el nuevo cliente
        }
        print(f"DEBUG: Parámetros para inserción: {params}")
        
        result = db.execute(query_clone, params)
        db.commit()
        
        # Retornar cliente clonado
        nuevo_cliente_id = result.lastrowid
        print(f"DEBUG: Cliente clonado con ID: {nuevo_cliente_id}")
        return obtener_cliente(nuevo_cliente_id, db)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Error inesperado: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")