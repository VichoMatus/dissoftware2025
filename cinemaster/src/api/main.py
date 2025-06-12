
from fastapi import FastAPI
import uvicorn
import threading

# Crear la instancia de FastAPI
app = FastAPI(
    title="CineMaster API",
    description="API para gestión de cine",
    version="1.0.0"
)

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