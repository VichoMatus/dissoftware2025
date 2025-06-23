from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.auth_controller import AuthController
from models.database import SessionLocal

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_type: str = None
    user_data: dict = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        cliente = AuthController.login_cliente(db, email, password)
        if cliente:
            return LoginResponse(
                success=True,
                message="Login como Cliente completado!",
                user_type="cliente",
                user_data={
                    "id": cliente.cliente_id,
                    "nombre": cliente.nombre,
                    "email": cliente.Email,
                    "membership": cliente.Membership
                }
            )
        
        # Intentar login como empleado
        empleado = AuthController.login_empleado(db, email, password)
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
        admin = AuthController.login_admin(db, email, password)
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

@router.post("/register", response_model=dict)
async def register(request: LoginRequest, db: Session = Depends(get_db)):
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
        
        # Por ahora usamos el email como nombre, se puede modificar después
        nombre = email.split("@")[0]
        
        cliente = AuthController.register_cliente(db, nombre, email, password, False)
        
        return {
            "success": True,
            "message": f"Cliente {cliente.nombre} registrado exitosamente!",
            "cliente": {
                "id": cliente.cliente_id,
                "nombre": cliente.nombre,
                "email": cliente.Email,
                "membership": cliente.Membership
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )
