import customtkinter as ctk
from PIL import Image, ImageTk
import os
import requests
from datetime import datetime
from tkinter import messagebox

from views.reservations.reservation_view import open_reservation_view
from views.Cartelera_Solid.profile_button import ProfileButton
from views.Cartelera_Solid.cartel_clasico import CartelClasico
from services.booking_facade import BookingFacade
from adapters.pelicula_adapter import PeliculaAdapter

class MainView(ctk.CTk):
    def __init__(self, cliente, dashboard_logger=None):
        super().__init__()

        self.title("Cine Management")
        self.geometry("1280x720")
        ctk.set_appearance_mode("dark")

        self.cliente = cliente
        self.dashboard_logger = dashboard_logger

        # Header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill='x', padx=20, pady=10)

        current_dir = os.path.dirname(__file__)
        logo_path = os.path.join(current_dir, "images", "logo.png")
        self.logo_image = Image.open(logo_path)
        self.logo_image = self.logo_image.resize((100, 100))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = ctk.CTkLabel(self.header_frame, image=self.logo_photo, text="")
        self.logo_label.pack(side="left", padx=10)

        self.app_name_label = ctk.CTkLabel(self.header_frame, text="CineMaster", font=("Arial", 24, "bold"))
        self.app_name_label.pack(side="left", padx=10)

        self.profile_button = ProfileButton(self.header_frame, self.cliente)

        # Cartelera
        self.cartelera_frame = ctk.CTkFrame(self, corner_radius=10)
        self.cartelera_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Obtener películas EXCLUSIVAMENTE desde la API
        peliculas = self.get_peliculas_from_api()

        self.carteles = []
        for i, pelicula in enumerate(peliculas):
            cartel = CartelClasico(self.cartelera_frame, pelicula, self.cliente, self.reserve_movie)
            cartel.grid(row=0, column=i, padx=20)
            self.carteles.append(cartel)

    def get_peliculas_from_api(self):
        """Obtiene las películas EXCLUSIVAMENTE desde la API"""
        try:
            response = requests.get("http://127.0.0.1:8000/cartelera/")
            if response.status_code == 200:
                peliculas_data = response.json()
                return PeliculaAdapter.from_api_list(peliculas_data)
            else:
                print(f"❌ Error al obtener películas desde API: {response.status_code}")
                messagebox.showerror("Error", f"No se pudieron cargar las películas desde la API. Código: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error conectando con la API: {e}")
            messagebox.showerror("Error de Conexión", "No se pudo conectar con la API para obtener las películas.")
            return []

    def get_horarios_from_api(self, pelicula_id):
        """Obtiene los horarios EXCLUSIVAMENTE desde la API"""
        try:
            response = requests.get(f"http://127.0.0.1:8000/cartelera/{pelicula_id}/horarios")
            if response.status_code == 200:
                horarios_data = response.json()
                horarios_with_ids = []
                for horario in horarios_data:
                    fecha_dt = datetime.fromisoformat(horario['fecha'].replace('Z', '+00:00')) if horario['fecha'] else None
                    horarios_with_ids.append((horario['id'], fecha_dt))
                return horarios_with_ids
            else:
                print(f"❌ Error al obtener horarios desde API: {response.status_code}")
                messagebox.showerror("Error", f"No se pudieron cargar los horarios desde la API. Código: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error conectando con la API para horarios: {e}")
            messagebox.showerror("Error de Conexión", "No se pudo conectar con la API para obtener los horarios.")
            return []

    def reserve_movie(self, pelicula, showtimes_with_ids, cliente):
        # Obtener horarios EXCLUSIVAMENTE desde la API
        horarios_api = self.get_horarios_from_api(pelicula.id_pelicula)
        
        if not horarios_api:
            messagebox.showerror("Error", "No se pudieron cargar los horarios para esta película.")
            return
        
        # Registrar selección de película en el dashboard
        if self.dashboard_logger:
            self.dashboard_logger.log_movie_selection(
                pelicula.Title, 
                getattr(pelicula, 'id_pelicula', None)
            )
        
        reservation_system = BookingFacade()
        self.destroy()
        open_reservation_view(
            pelicula.Title, pelicula.Duration, pelicula.Gender, pelicula.Image_path, 
            horarios_api,  # Usar horarios EXCLUSIVAMENTE de la API
            cliente, reservation_system
        )