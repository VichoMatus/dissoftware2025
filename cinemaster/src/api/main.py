from fastapi import FastAPI
import uvicorn
import threading
import webbrowser
import time
from api.trabajador_api.clientes_api import router as clientes_router
from api.trabajador_api.peliculas_api import router as peliculas_router
from api.trabajador_api.reservas_api import router as reservas_router
from api.trabajador_api.funciones_api import router as funciones_router
from api.trabajador_api.promociones_api import router as promociones_router

# Importar routers
try:
    # ---- MODIFICACIÓN AQUÍ ----
    from .routers import login, auth, dashboard, api_profile_router # [NUEVO] Se añade el router del perfil
    from .routers import api_admin_router # [ADMIN] Se añade el router del admin
except ImportError:
    # Fallback para importación absoluta cuando se ejecuta directamente
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    # ---- MODIFICACIÓN AQUÍ ----
    from routers import login, auth, dashboard, api_profile_router # [NUEVO] Se añade el router del perfil
    from routers import api_admin_router # [ADMIN] Se añade el router del admin

# Crear la instancia de FastAPI
app = FastAPI(
    title="CineMaster API",
    description="API para gestión de cine",
    version="1.0.0"
)

# Incluir routers
app.include_router(login.router)
app.include_router(auth.router)
app.include_router(dashboard.router)

app.include_router(clientes_router)
app.include_router(peliculas_router)
app.include_router(reservas_router)
app.include_router(funciones_router)
app.include_router(promociones_router)

# ---- MODIFICACIÓN AQUÍ ----
app.include_router(api_profile_router.router) # [NUEVO] Se registra el router para que las rutas /profile/... funcionen
app.include_router(api_admin_router.router)   # [ADMIN] Se registra el router para que las rutas /admin/... funcionen


@app.get("/")
async def root():
    return {"message": "CineMaster API v1.0.0 está funcionando!"}

@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "API funcionando correctamente"}

def start_api():
    """Función para iniciar la API en un hilo separado"""
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def start_api_in_thread():
    """Inicia la API en un hilo separado para no bloquear la aplicación principal"""
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()
    return api_thread

def open_browser_delayed():
    """Abre el navegador después de un pequeño delay para asegurar que la API esté lista"""
    time.sleep(2)  # Esperar 2 segundos para que la API esté lista
    webbrowser.open("http://127.0.0.1:8000/login/")

def start_api_with_browser():
    """Inicia la API y abre el navegador automáticamente"""
    # Iniciar API en hilo separado
    api_thread = start_api_in_thread()
    
    # Abrir navegador en otro hilo
    browser_thread = threading.Thread(target=open_browser_delayed, daemon=True)
    browser_thread.start()
    
    return api_thread

if __name__ == "__main__":
    # Si se ejecuta directamente, iniciar la API y abrir navegador
    print(" Iniciando CineMaster API...")
    print(" La página de bienvenida se abrirá automáticamente en tu navegador")
    start_api_with_browser()
    
    # Mantener el programa principal ejecutándose
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Cerrando CineMaster API...")