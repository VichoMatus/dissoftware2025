import customtkinter as ctk
import tkinter.messagebox as tkmb
from reservations.seat_selection import SeatSelection  # Importamos la vista de selección de asiento

class ReservationView(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky="nsew")

        self.create_widgets()

    def create_widgets(self):
        # Título principal
        self.title_label = ctk.CTkLabel(self, text="¡Reserva tu Película!", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, pady=20)

        # Etiqueta para seleccionar la película
        self.movie_label = ctk.CTkLabel(self, text="Seleccione el nombre de la película:", font=("Arial", 14))
        self.movie_label.grid(row=1, column=0, pady=10)

        # Lista de películas disponibles
        self.movies_list = ["Película 1", "Película 2", "Película 3", "Película 4", "Película 5"]
        
        # Crear un dropdown (CTkOptionMenu) para seleccionar la película
        self.movie_dropdown = ctk.CTkOptionMenu(self, values=self.movies_list, font=("Arial", 14))
        self.movie_dropdown.grid(row=2, column=0, pady=10, padx=20, ipadx=10)

        # Botón para realizar la reserva con un diseño más atractivo
        self.reserve_button = ctk.CTkButton(self, text="Reservar", command=self.reserve_movie, font=("Arial", 16), 
                                            fg_color="#4CAF50", hover_color="#45a049", width=200)
        self.reserve_button.grid(row=3, column=0, pady=20)

        # Etiqueta de éxito (inicialmente oculta)
        self.success_label = ctk.CTkLabel(self, text="", text_color="green", font=("Arial", 14))
        self.success_label.grid(row=4, column=0, pady=10)

        # Botón para elegir un asiento (inicialmente deshabilitado)
        self.select_seat_button = ctk.CTkButton(self, text="Seleccionar Asiento", command=self.select_seat, state="disabled", 
                                                 font=("Arial", 16), fg_color="#4CAF50", hover_color="#45a049", width=200)
        self.select_seat_button.grid(row=5, column=0, pady=20)

        # Ajustar el diseño de la ventana para que ocupe todo el espacio disponible
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def reserve_movie(self):
        # Obtener el nombre de la película seleccionada desde el dropdown
        movie_name = self.movie_dropdown.get()

        if movie_name:  # Si el usuario seleccionó una película
            # Mostrar mensaje de éxito
            self.success_label.configure(text=f"Reserva realizada para: {movie_name}")
            self.success_label.grid(row=4, column=0, pady=10)  # Mostrar mensaje de éxito
            
            # Mostrar alerta de éxito con tkinter.messagebox
            tkmb.showinfo("Éxito", f"La reserva para '{movie_name}' fue realizada con éxito.")
            
            # Habilitar el botón para seleccionar asiento
            self.select_seat_button.configure(state="normal")
        else:
            # Si no se selecciona una película
            self.success_label.configure(text="Por favor selecciona una película.")
            self.success_label.grid(row=4, column=0, pady=10)  # Mostrar mensaje de error

    def select_seat(self):
        # Llamar a la vista de selección de asiento
        self.seat_selection_view = SeatSelection(self.master)
        self.seat_selection_view.grid(row=0, column=0, sticky="nsew")
        self.grid_forget()  # Ocultar la vista de reserva
