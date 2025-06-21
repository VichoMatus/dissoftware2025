from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

@router.get("/", response_class=HTMLResponse)
async def login_page():
    """Página de bienvenida/login"""
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CineMaster - Bienvenida</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
            }
            
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                padding: 60px 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                max-width: 500px;
                width: 90%;
            }
            
            .logo {
                font-size: 3.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            .title {
                font-size: 2.5em;
                font-weight: 700;
                margin-bottom: 20px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }
            
            .subtitle {
                font-size: 1.2em;
                margin-bottom: 30px;
                opacity: 0.9;
            }
            
            .welcome-text {
                font-size: 1.5em;
                font-weight: 600;
                color: #FFD700;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
                animation: glow 2s ease-in-out infinite alternate;
            }
            
            @keyframes glow {
                from { text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5), 0 0 10px #FFD700; }
                to { text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5), 0 0 20px #FFD700, 0 0 30px #FFD700; }
            }
            
            .features {
                margin-top: 30px;
                text-align: left;
                display: inline-block;
            }
            
            .feature {
                margin: 10px 0;
                font-size: 1.1em;
            }
            
            .feature::before {
                content: "🎬 ";
                margin-right: 10px;
            }
            
            .status {
                margin-top: 30px;
                padding: 15px;
                background: rgba(0, 255, 0, 0.2);
                border-radius: 10px;
                border: 1px solid rgba(0, 255, 0, 0.3);
            }
            
            .status-text {
                color: #90EE90;
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🎭</div>
            <h1 class="title">CineMaster</h1>
            <p class="subtitle">Sistema de Gestión de Cine</p>
            
            <div class="welcome-text">
                ¡Bienvenido!
            </div>
            
            <div class="features">
                <div class="feature">Gestión de películas y funciones</div>
                <div class="feature">Reserva de asientos en tiempo real</div>
                <div class="feature">Sistema de pagos integrado</div>
                <div class="feature">Administración completa</div>
                <div class="feature">Notificaciones automáticas</div>
            </div>
            
            <div class="status">
                <div class="status-text">🟢 API en funcionamiento</div>
            </div>
        </div>
        
        <script>
            // Agregar un poco de interactividad
            document.addEventListener('DOMContentLoaded', function() {
                const container = document.querySelector('.container');
                
                container.addEventListener('mouseenter', function() {
                    this.style.transform = 'scale(1.02)';
                    this.style.transition = 'transform 0.3s ease';
                });
                
                container.addEventListener('mouseleave', function() {
                    this.style.transform = 'scale(1)';
                });
            });
        </script>
    </body>
    </html>
    """
    return html_content

@router.get("/status")
async def login_status():
    """Estado del sistema de login"""
    return {
        "status": "active",
        "message": "Sistema de login funcionando correctamente",
        "features": [
            "Autenticación de usuarios",
            "Gestión de sesiones",
            "Página de bienvenida"
        ]
    }
