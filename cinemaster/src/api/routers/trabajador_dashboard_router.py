from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

router = APIRouter(prefix="/trabajador-dashboard", tags=["Dashboard Trabajador"])

# Store para mantener el estado del trabajador actual y su historial
trabajador_session = {
    "current_trabajador": None,
    "action_history": []
}

class TrabajadorAction(BaseModel):
    action_type: str
    description: str
    timestamp: str
    details: Dict[str, Any] = {}

class TrabajadorLogin(BaseModel):
    trabajador_name: str
    trabajador_id: int
    email: str

@router.post("/login")
async def set_current_trabajador(trabajador_data: TrabajadorLogin):
    """Establece el trabajador actual en el dashboard"""
    global trabajador_session

    trabajador_session["current_trabajador"] = {
        "name": trabajador_data.trabajador_name,
        "id": trabajador_data.trabajador_id,
        "email": trabajador_data.email,
        "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Agregar acción de login
    login_action = {
        "action_type": "LOGIN",
        "description": f"Trabajador {trabajador_data.trabajador_name} ha iniciado sesión",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "details": {
            "trabajador_id": trabajador_data.trabajador_id,
            "email": trabajador_data.email
        }
    }

    trabajador_session["action_history"].append(login_action)

    return {"success": True, "message": "Trabajador establecido en dashboard"}

@router.post("/log-action")
async def log_trabajador_action(action: TrabajadorAction):
    """Registra una acción del trabajador"""
    global trabajador_session

    action_dict = {
        "action_type": action.action_type,
        "description": action.description,
        "timestamp": action.timestamp,
        "details": action.details
    }

    trabajador_session["action_history"].append(action_dict)

    return {"success": True, "message": "Acción registrada"}

@router.get("/", response_class=HTMLResponse)
async def get_trabajador_dashboard():
    """Muestra el dashboard con información del trabajador actual"""
    global trabajador_session

    current_trabajador = trabajador_session.get("current_trabajador")
    history = trabajador_session.get("action_history", [])

    # Construir HTML del dashboard
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CineMaster - Dashboard Trabajador</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #8e24aa 0%, #3949ab 100%);
                color: white;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 30px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            .welcome {{
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }}
            .trabajador-info {{
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 30px;
            }}
            .history-section {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 20px;
            }}
            .history-title {{
                font-size: 1.5rem;
                margin-bottom: 20px;
                border-bottom: 2px solid rgba(255, 255, 255, 0.3);
                padding-bottom: 10px;
            }}
            .action-item {{
                background: rgba(255, 255, 255, 0.1);
                margin-bottom: 10px;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #8e24aa;
            }}
            .action-time {{
                font-size: 0.9rem;
                opacity: 0.8;
                margin-bottom: 5px;
            }}
            .action-description {{
                font-size: 1.1rem;
                font-weight: 500;
            }}
            .action-details {{
                font-size: 0.9rem;
                opacity: 0.7;
                margin-top: 5px;
            }}
            .no-trabajador {{
                text-align: center;
                font-size: 1.5rem;
                color: #ffeb3b;
            }}
            .refresh-btn {{
                background: #8e24aa;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1rem;
                margin-top: 20px;
            }}
            .refresh-btn:hover {{
                background: #6d1b7b;
            }}
        </style>
        <script>
            // Auto-refresh cada 5 segundos
            setTimeout(function(){{
                location.reload();
            }}, 5000);
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛠️ CineMaster Dashboard Trabajador</h1>
    """

    if current_trabajador:
        html_content += f"""
                <div class="welcome">
                    ¡Bienvenido {current_trabajador['name']}!
                </div>
                <div class="trabajador-info">
                    <p><strong>ID Trabajador:</strong> {current_trabajador['id']}</p>
                    <p><strong>Email:</strong> {current_trabajador['email']}</p>
                    <p><strong>Sesión iniciada:</strong> {current_trabajador['login_time']}</p>
                </div>
                <div class="acciones-section">
                    <h2>⚡ Acciones disponibles para el trabajador</h2>
                    <ul>
                        <li>Listar promociones</li>
                        <li>Crear promoción</li>
                        <li>Actualizar promoción</li>
                        <li>Eliminar promoción</li>
                        <!-- Agrega aquí las acciones de otros servicios -->
                    </ul>
                </div>
            </div>
            
            <div class="history-section">
                <div class="history-title">📋 Historial de Acciones</div>
        """

        if history:
            # Mostrar las últimas 10 acciones
            recent_actions = history[-10:]
            recent_actions.reverse()  # Mostrar las más recientes primero

            for action in recent_actions:
                details_str = ""
                if action.get("details"):
                    details_list = [f"{k}: {v}" for k, v in action["details"].items()]
                    details_str = f"<div class='action-details'>{' | '.join(details_list)}</div>"

                html_content += f"""
                <div class="action-item">
                    <div class="action-time">⏰ {action['timestamp']}</div>
                    <div class="action-description">{action['description']}</div>
                    {details_str}
                </div>
                """
        else:
            html_content += "<p>No hay acciones registradas aún.</p>"

        html_content += "</div>"
    else:
        html_content += f"""
                <div class="no-trabajador">
                    🔐 No hay trabajador conectado actualmente
                </div>
            </div>
        """

    html_content += """
            <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar</button>
        </div>
    </body>
    </html>
    """

    return html_content

@router.get("/clear")
async def clear_trabajador_dashboard():
    """Limpia el dashboard del trabajador"""
    global trabajador_session
    trabajador_session = {
        "current_trabajador": None,
        "action_history": []
    }
    return {"success": True, "message": "Dashboard de trabajador limpiado"}