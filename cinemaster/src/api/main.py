
from fastapi import FastAPI
import uvicorn
import threading
from api.trabajador_api.clientes_api import router as clientes_router
from api.trabajador_api.peliculas_api import router as peliculas_router
from api.trabajador_api.reservas_api import router as reservas_router
from api.trabajador_api.funciones_api import router as funciones_router
from api.trabajador_api.promociones_api import router as promociones_router

# Crear la instancia de FastAPI
app = FastAPI(
    title="CineMaster API",
    description="API para gestión de cine",
    version="1.0.0"
)

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

if __name__ == "__main__":
    # Si se ejecuta directamente, iniciar solo la API
    start_api()