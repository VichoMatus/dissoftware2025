import customtkinter as ctk
import threading
from controllers.app_controller import AppController

def check_api_port():
    """Verifica si el puerto de la API está disponible"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()
        return result == 0
    except:
        return False

def start_api():
    """Inicia la API importando y ejecutando su función principal"""
    try:
        from api.main import start_api_in_thread
        print("🚀 Iniciando API CineMaster...")
        start_api_in_thread()  # Solo iniciar la API, sin abrir navegador
    except Exception as e:
        print(f"❌ Error al iniciar la API: {e}")

# --- Eliminamos la función open_browser_after_delay y su uso ---

def main():
    ctk.set_appearance_mode("dark")
    
    print("🎬 Iniciando CineMaster...")
    print("🏗️  Arquitectura: Aplicación → API → Base de Datos")
    print("=" * 50)
    
    # Iniciar la API en segundo plano
    print("🚀 Iniciando CineMaster API en http://127.0.0.1:8000")
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()
    print("✅ API iniciada correctamente!")
    
    # --- Ya NO abrimos el navegador automáticamente ---
    
    print("🖥️  Iniciando aplicación de escritorio...")
    print("=" * 50)
    
    # Iniciar la aplicación principal
    app_controller = AppController()
    app_controller.start()

if __name__ == "__main__":
    main()