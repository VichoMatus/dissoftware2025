import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os
# Agregar el directorio de la aplicación para que pueda encontrar los módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from models.movie import get_all_movies
from models.database import get_db
from views.reservations.seat_selection import open_seat_selection_view  # Importamos la función de seat_selection.py


class ReservationView(ctk.CTk):
    def __init__(self, selected_movie_Title, selected_movie_Duration, selected_movie_Gender, movie_image_path, showtimes_with_ids, open_cartelera_view):
        super().__init__()

        self.title("Cine Master")
        self.geometry("1280x720")  # Ajustar el tamaño de la ventana
        self.resizable(True, True)  # Permitir que la ventana sea redimensionable

        # Configurar el modo oscuro
        ctk.set_appearance_mode("dark")

        # Obtener la película desde la base de datos usando el ID
        self.open_cartelera_view = open_cartelera_view
        self.selected_movie_Title = selected_movie_Title
        self.selected_movie_Duration = selected_movie_Duration
        self.selected_movie_Gender = selected_movie_Gender
        self.movie_image_path = movie_image_path
        self.showtimes_with_ids = showtimes_with_ids
        
        # Crear los dos frames
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill='x', padx=20, pady=10)

        # Crear un frame principal que contendrá toda la interfaz
        self.reservation_frame = ctk.CTkFrame(self)
        self.reservation_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Crear los widgets dentro de este frame
        self.create_widgets()

    def create_widgets(self):



        # Frame para el header
        current_dir = os.path.dirname(__file__)  # Obtiene el directorio actual
        logo_path = os.path.join(current_dir, "..", "images", "logo.png")  # Ruta correcta

        self.logo_image = Image.open(logo_path)  # Ajustamos la ruta aquí
        self.logo_image = self.logo_image.resize((100, 100))  # Redimensionar si es necesario
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        
        self.logo_label = ctk.CTkLabel(self.header_frame, image=self.logo_photo, text="")  # Corregido para evitar texto
        self.logo_label.pack(side="left", padx=10)

        self.app_name_label = ctk.CTkLabel(self.header_frame, text="CineMaster", font=("Arial", 24, "bold"))
        self.app_name_label.pack(side="left", padx=10)

        # Cargar y mostrar la imagen de la película
        self.load_movie_image(self.movie_image_path)

        # Detalles de la película (alineados al borde de la pantalla)
        self.movie_title_label = ctk.CTkLabel(self.reservation_frame, text=f"Nombre de la película: {self.selected_movie_Title}")
        self.movie_title_label.grid(row=1, column=1, padx=20, pady=10, sticky="w", columnspan=3)

        self.movie_duration_label = ctk.CTkLabel(self.reservation_frame, text=f"Duración: {self.selected_movie_Duration} min")
        self.movie_duration_label.grid(row=2, column=1, padx=20, pady=10, sticky="w", columnspan=3)

        self.movie_genre_label = ctk.CTkLabel(self.reservation_frame, text=f"Género: {self.selected_movie_Gender}")
        self.movie_genre_label.grid(row=3, column=1, padx=20, pady=10, sticky="w", columnspan=3)

        # Mostrar el dropdown de horarios
        self.showtimes_label = ctk.CTkLabel(self.reservation_frame, text="Horarios disponibles:")
        self.showtimes_label.grid(row=1, column=9, padx=20, pady=10, sticky="w", columnspan=3)

        # Convertir las tuplas (id, fecha) a una lista de cadenas legibles
        self.showtimes_strings = [f"{showtime[1].strftime('%Y-%m-%d %H:%M')} - ID: {showtime[0]}" for showtime in self.showtimes_with_ids]

        # Dropdown (OptionMenu) para seleccionar el horario
        self.selected_showtime = ctk.StringVar(value=self.showtimes_strings[0])  # Valor por defecto
        self.showtime_dropdown = ctk.CTkOptionMenu(self.reservation_frame, variable=self.selected_showtime, values=self.showtimes_strings)
        self.showtime_dropdown.grid(row=2, column=9, padx=20, pady=10, sticky="w", columnspan=3)


        # Botón para agendar reserva (alineado a la izquierda, ajustado al tamaño de la pantalla)
        self.reserve_button = ctk.CTkButton(self.reservation_frame, text="Agendar reserva", width=200, height=40, command=self.reserve_movie)
        self.reserve_button.grid(row=5, column=6, padx=20, pady=20, columnspan=3, sticky="w")

    def load_movie_image(self, image_path):
        #Asegurarnos de que la ruta de la imagen sea valida
        try:
            # Cargar y redimensionar la imagen
            movie_image = Image.open(image_path)
            movie_image = movie_image.resize((500, 400))  # Redimensionar la imagen a 500x400
            movie_image_tk = ImageTk.PhotoImage(movie_image)

            # Crear un widget CTkLabel con la imagen
            self.movie_image_label = ctk.CTkLabel(self.reservation_frame, image=movie_image_tk, text="")
            self.movie_image_label.grid(row=1, column=0, padx=0, pady=20, rowspan=3, sticky="n")

            # Mantener una referencia de la imagen para evitar que se pierda
            self.movie_image_label.image = movie_image_tk

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
    
    def reserve_movie(self):
        selected_showtime_string = self.selected_showtime.get()

        # Verificar que haya un valor seleccionado
        if not selected_showtime_string:
            messagebox.showerror("Error", "No se ha seleccionado un horario válido.")
            return

        # Extraemos el ID y la fecha del showtime seleccionado
        selected_showtime_id = None
        selected_showtime_date = None
    
        for showtime in self.showtimes_with_ids:
            showtime_string = f"{showtime[1].strftime('%Y-%m-%d %H:%M')} - ID: {showtime[0]}"
            if selected_showtime_string == showtime_string:
                selected_showtime_id = showtime[0]
                selected_showtime_date = showtime[1]
                break

        if selected_showtime_id is None:
            messagebox.showerror("Error", "No se ha seleccionado un horario válido.")
            return

        messagebox.showinfo("Reserva Confirmada", f"Reserva realizada para la película: {self.selected_movie_Title}\nHorario: {selected_showtime_string}")

        # Destruir la ventana de reserva (cerrar la ventana actual)
        self.destroy()

        # Llamar a la vista de selección de asientos y pasarle el ID del horario seleccionado
        open_seat_selection_view(selected_showtime_id, selected_showtime_date)  # Pasamos el ID y la fecha



# Ejecutar la aplicación
def open_reservation_view(selected_movie_Title, selected_movie_Duration, selected_movie_Gender, movie_image_path, showtimes_with_ids, close_cartelera_callback):
    app = ReservationView(selected_movie_Title, selected_movie_Duration, selected_movie_Gender, movie_image_path, showtimes_with_ids, close_cartelera_callback)
    app.mainloop()
    close_cartelera_callback()


