import customtkinter as ctk
from views.authentication.login_view import LoginView
from reservations.reservation_view import ReservationView

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración del modo oscuro y color azul
        ctk.set_appearance_mode("dark")  # Modo oscuro
        ctk.set_default_color_theme("blue")  # Color azul

        self.title("Sistema de Reservas de Cine")
        self.geometry("800x600")  # Tamaño de ventana ajustado

        self.create_widgets()

    def create_widgets(self):
        # Añadir una imagen o logo en la parte superior
        self.logo = ctk.CTkLabel(self, text="🎥 Sistema de Reservas de Cine 🎬", font=("Arial", 24, "bold"))
        self.logo.grid(row=0, column=0, pady=20)

        # Botón para ver las reservas con un diseño más atractivo
        self.reservation_button = ctk.CTkButton(self, text="Ver Reservas", command=self.show_reservations, 
                                                 font=("Arial", 16), fg_color="#4CAF50", hover_color="#45a049", width=200)
        self.reservation_button.grid(row=1, column=0, pady=20)

        # Añadir un pequeño mensaje explicativo
        self.info_label = ctk.CTkLabel(self, text="¡Haz clic para ver las reservas disponibles!", font=("Arial", 14), text_color="gray")
        self.info_label.grid(row=2, column=0, pady=10)

        # Configurar el diseño de la ventana para que ocupe todo el espacio disponible
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_reservations(self):
        # Deshabilitar el botón "Ver Reservas" mientras se realiza el proceso de selección de asiento
        self.reservation_button.configure(state="disabled")

        # Añadir una animación suave para ocultar los widgets de la vista principal
        self.logo.grid_forget()
        self.reservation_button.grid_forget()
        self.info_label.grid_forget()

        # Llama a la vista de reservas
        self.reservation_view = ReservationView(self)

        # Mostrar la vista de reservas en el espacio disponible
        self.reservation_view.grid(row=0, column=0, sticky="nsew")



# Este bloque inicializa la aplicación
if __name__ == "__main__":
    #app = MainView()  # Crear una instancia de la ventana principal
    #app.mainloop()  # Iniciar el ciclo de eventos de la interfaz gráfica


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cine Management System")
        self.geometry("1000x720")

        # Mostramos la vista de inicio de sesión por defecto
        self.login_view = LoginView(self)

if __name__ == "__main__":
    #app = Application()
    #app.mainloop()
