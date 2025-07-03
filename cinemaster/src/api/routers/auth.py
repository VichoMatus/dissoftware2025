from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.schemas.auth_schemas import (
    LoginRequest, 
    LoginResponse, 
    RegisterRequest, 
    RegisterResponse
)
from api.database import get_db

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint para autenticar usuarios (clientes, empleados, administradores)
    """
    try:
        email = request.email.strip()
        password = request.password.strip()
        
        if "@" not in email:
            raise HTTPException(
                status_code=400, 
                detail="El correo electrónico debe contener '@'"
            )
        
        # Intentar login como cliente
        query_cliente = text("SELECT cliente_id, nombre, Email, Membership FROM Cliente WHERE Email = :email AND Password = :password")
        result = db.execute(query_cliente, {"email": email, "password": password})
        cliente = result.fetchone()
        
        if cliente:
            return LoginResponse(
                success=True,
                message="Login como Cliente completado!",
                user_type="cliente",
                user_data={
                    "id": cliente.cliente_id,
                    "nombre": cliente.nombre,
                    "email": cliente.Email,
                    "membership": bool(cliente.Membership)
                }
            )
        
        # Intentar login como empleado
        query_empleado = text("SELECT employee_id, Name, Email FROM Empleado WHERE Email = :email AND Password = :password")
        result = db.execute(query_empleado, {"email": email, "password": password})
        empleado = result.fetchone()
        
        if empleado:
            return LoginResponse(
                success=True,
                message="Login como Empleado completado",
                user_type="empleado",
                user_data={
                    "id": empleado.employee_id,
                    "name": empleado.Name,
                    "email": empleado.Email
                }
            )
        
        # Intentar login como administrador
        query_admin = text("SELECT Admin_id, nombre, Email FROM Admin WHERE Email = :email AND Password = :password")
        result = db.execute(query_admin, {"email": email, "password": password})
        admin = result.fetchone()
        
        if admin:
            return LoginResponse(
                success=True,
                message="Login como Admin completado!",
                user_type="admin",
                user_data={
                    "id": admin.Admin_id,
                    "nombre": admin.nombre,
                    "email": admin.Email
                }
            )
        
        # Si no se encontró ningún usuario
        raise HTTPException(
            status_code=401,
            detail="Email o contraseña incorrecta"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Endpoint para registrar nuevos clientes
    """
    try:
        email = request.email.strip()
        password = request.password.strip()
        
        if "@" not in email:
            raise HTTPException(
                status_code=400,
                detail="El correo electrónico debe contener '@'"
            )
        
        if len(password) < 4:
            raise HTTPException(
                status_code=400,
                detail="La contraseña debe tener al menos 4 caracteres"
            )
        
        # Verificar si el email ya existe
        query_existe = text("SELECT cliente_id FROM Cliente WHERE Email = :email")
        result = db.execute(query_existe, {"email": email})
        cliente_existente = result.fetchone()
        
        if cliente_existente:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un cliente con ese email"
            )
        
        # Por ahora usamos el email como nombre, se puede modificar después
        nombre = request.nombre if request.nombre else email.split("@")[0]
        
        # Crear nuevo cliente
        query_crear = text("""
            INSERT INTO Cliente (nombre, Email, Password, Membership, Reservation_history)
            VALUES (:nombre, :email, :password, :membership, :history)
        """)
        
        result = db.execute(query_crear, {
            "nombre": nombre,
            "email": email,
            "password": password,
            "membership": False,
            "history": ""
        })
        db.commit()
        
        # Obtener el cliente creado
        cliente_id = result.lastrowid
        query_cliente = text("SELECT cliente_id, nombre, Email, Membership FROM Cliente WHERE cliente_id = :id")
        result = db.execute(query_cliente, {"id": cliente_id})
        cliente = result.fetchone()
        
        return RegisterResponse(
            success=True,
            message=f"Cliente {cliente.nombre} registrado exitosamente!",
            cliente={
                "id": cliente.cliente_id,
                "nombre": cliente.nombre,
                "email": cliente.Email,
                "membership": bool(cliente.Membership)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )
