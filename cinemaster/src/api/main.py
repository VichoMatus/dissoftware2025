from fastapi import FastAPI
import uvicorn
import threading
import time
from api.trabajador_api.clientes_api import router as clientes_router
from api.trabajador_api.peliculas_api import router as peliculas_router
from api.trabajador_api.reservas_api import router as reservas_router
from api.trabajador_api.funciones_api import router as funciones_router
from api.trabajador_api.promociones_api import router as promociones_router

# Importar routers
try:
    from .routers import login, auth, dashboard
except ImportError:
    # Fallback para importación absoluta cuando se ejecuta directamente
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from routers import login, auth, dashboard

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

# --- El navegador ya NO se abrirá automáticamente ---
# (Dejo la función por si la quieres en desarrollo, pero no se llama abajo)
def open_browser_delayed():
    import webbrowser
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000/login/")

def start_api_with_browser():
    api_thread = start_api_in_thread()
    browser_thread = threading.Thread(target=open_browser_delayed, daemon=True)
    browser_thread.start()
    return api_thread

if __name__ == "__main__":
    print("🚀 Iniciando CineMaster API...")
    start_api()  # <-- Solo inicia la API en modo backend puro

    # Mantener el programa principal ejecutándose (aunque uvicorn ya bloquea)
    # Puedes comentar el loop si ves que no es necesario.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Cerrando CineMaster API...")