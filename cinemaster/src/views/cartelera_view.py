import customtkinter as ctk
from PIL import Image, ImageTk
import os

from models.movie import get_all_movies
from models.database import get_db
from models.cliente import Cliente
from views.reservations.reservation_view import open_reservation_view
from views.Cartelera_Solid.profile_button import ProfileButton
from views.Cartelera_Solid.cartel_clasico import CartelClasico
from services.booking_facade import BookingFacade

# Importa el cartel clásico desde la nueva estructura OCP
from views.Cartelera_Solid.cartel_clasico import CartelClasico

class MainView(ctk.CTk):
    def __init__(self, cliente):
        super().__init__()

        self.title("Cine Management")
        self.geometry("1280x720")
        ctk.set_appearance_mode("dark")

        self.cliente = cliente

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

        self.db_session = next(get_db())
        peliculas = get_all_movies(self.db_session)

        self.carteles = []
        for i, pelicula in enumerate(peliculas):
            cartel = CartelClasico(self.cartelera_frame, pelicula, self.cliente, self.reserve_movie)
            cartel.grid(row=0, column=i, padx=20)
            self.carteles.append(cartel)

    def reserve_movie(self, pelicula, showtimes_with_ids, cliente):
        reservation_system = BookingFacade()  # Instancia del sistema de reservas
        self.destroy()
        open_reservation_view(
            pelicula.Title, pelicula.Duration, pelicula.Gender, pelicula.Image_path, showtimes_with_ids, cliente, reservation_system
        )