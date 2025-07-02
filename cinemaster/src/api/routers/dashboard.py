from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Store para mantener el estado del cliente actual y su historial
client_session = {
    "current_client": None,
    "action_history": []
}

class ClientAction(BaseModel):
    action_type: str
    description: str
    timestamp: str
    details: Dict[str, Any] = {}

class ClientLogin(BaseModel):
    client_name: str
    client_id: int
    email: str

@router.post("/client-login")
async def set_current_client(client_data: ClientLogin):
    """Establece el cliente actual en el dashboard"""
    global client_session

    client_session["current_client"] = {
        "name": client_data.client_name,
        "id": client_data.client_id,
        "email": client_data.email,
        "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Agregar acción de login
    login_action = {
        "action_type": "LOGIN",
        "description": f"Cliente {client_data.client_name} ha iniciado sesión",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "details": {
            "client_id": client_data.client_id,
            "email": client_data.email
        }
    }

    client_session["action_history"].append(login_action)

    return {"success": True, "message": "Cliente establecido en dashboard"}

@router.post("/log-action")
async def log_client_action(action: ClientAction):
    """Registra una acción del cliente"""
    global client_session

    action_dict = {
        "action_type": action.action_type,
        "description": action.description,
        "timestamp": action.timestamp,
        "details": action.details
    }

    client_session["action_history"].append(action_dict)

    return {"success": True, "message": "Acción registrada"}

@router.get("/status")
async def get_dashboard_status():
    """Devuelve el estado actual del dashboard en formato JSON"""
    global client_session
    return {
        "current_client": client_session.get("current_client"),
        "action_history": client_session.get("action_history", [])
    }

@router.get("/clear")
async def clear_dashboard():
    """Limpia el dashboard"""
    global client_session
    client_session = {
        "current_client": None,
        "action_history": []
    }
    return {"success": True, "message": "Dashboard limpiado"}