import customtkinter as ctk
from controllers.app_controller import AppController
from api.main import start_api_in_thread

def main():
    ctk.set_appearance_mode("dark")
    
    # Iniciar la API en segundo plano
    print("Iniciando CineMaster API en http://127.0.0.1:8000")
    api_thread = start_api_in_thread()
    print("API iniciada correctamente!")
    print("Puedes acceder a:")
    print("- API: http://127.0.0.1:8000")
    print("- Documentación: http://127.0.0.1:8000/docs")
    
    # Iniciar la aplicación principal
    app_controller = AppController()
    app_controller.start()

if __name__ == "__main__":
    main()
