import customtkinter as ctk
import webbrowser
import time
import threading
import socket
from controllers.app_controller import AppController
from api.main import start_api_in_thread

def check_api_port():
    """Verifica si el puerto de la API está disponible"""
    try:
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
        from api.main import start_api_with_browser
        print("🚀 Iniciando API CineMaster...")
        start_api_with_browser()
    except Exception as e:
        print(f"❌ Error al iniciar la API: {e}")

def open_browser_after_delay():
    """Abre el navegador después de verificar que la API esté lista"""
    print("🔍 Verificando estado de la API...")
      # Esperar a que la API esté disponible
    max_attempts = 15
    for attempt in range(max_attempts):
        if check_api_port():
            print("✅ API detectada en el puerto 8000")
            time.sleep(1)  # Un pequeño delay adicional
            break
        time.sleep(0.5)
    
    try:
        webbrowser.open('http://127.0.0.1:8000/login/')
        print("🌐 Navegador abierto en: http://127.0.0.1:8000/login/")
        
        # Abrir el dashboard también en una nueva pestaña
        time.sleep(1)
        webbrowser.open('http://127.0.0.1:8000/dashboard/')
        print("📊 Dashboard abierto en: http://127.0.0.1:8000/dashboard/")
    except Exception as e:
        print(f"❌ Error al abrir el navegador: {e}")
        print("💡 Puedes abrir manualmente: http://127.0.0.1:8000/login/")

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
    
    # Abrir el navegador en un hilo separado
    browser_thread = threading.Thread(target=open_browser_after_delay, daemon=True)
    browser_thread.start()
    
    print("🖥️  Iniciando aplicación de escritorio...")
    print("📋 Enlaces disponibles:")
    print("   • Página de bienvenida: http://127.0.0.1:8000/login/")
    print("   • API: http://127.0.0.1:8000")
    print("   • Documentación: http://127.0.0.1:8000/docs")
    print("=" * 50)
    
    # Iniciar la aplicación principal
    app_controller = AppController()
    app_controller.start()

if __name__ == "__main__":
    main()
