from fastapi import APIRouter

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

@router.get("/status")
async def login_status():
    """Estado del sistema de login"""
    return {
        "status": "active",
        "message": "Sistema de login funcionando correctamente",
        "features": [
            "Autenticación de usuarios",
            "Gestión de sesiones"
        ]
    }