import customtkinter as ctk
from PIL import Image, ImageTk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from models.movie import get_all_movies  # Para obtener las películas desde la base de datos
from models.database import get_db  # Para obtener la sesión de la base de datos
from models.cliente import Cliente  # Importar Cliente desde models.cliente para usar la clase correcta
from views.reservations.reservation_view import open_reservation_view  # Importamos la vista de reserva

class MainView(ctk.CTk):
    def __init__(self, cliente):
        super().__init__()

        self.title("Cine Management")
        self.geometry("1280x720")
    
        # Configurar el modo oscuro
        ctk.set_appearance_mode("dark")

        # Guardamos el cliente logueado (debe ser instancia de models.cliente.Cliente)
        self.cliente = cliente

        # Crear los dos frames
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill='x', padx=20, pady=10)

        # Frame para el header
        current_dir = os.path.dirname(__file__)  # Obtiene el directorio actual
        logo_path = os.path.join(current_dir, "images", "logo.png")  # Ruta correcta

        self.logo_image = Image.open(logo_path)  # Ajustamos la ruta aquí
        self.logo_image = self.logo_image.resize((100, 100))  # Redimensionar si es necesario
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = ctk.CTkLabel(self.header_frame, image=self.logo_photo, text="")  # Corregido para evitar texto
        self.logo_label.pack(side="left", padx=10)

        self.app_name_label = ctk.CTkLabel(self.header_frame, text="CineMaster", font=("Arial", 24, "bold"))
        self.app_name_label.pack(side="left", padx=10)

        # Agregar botón con el nombre del cliente logueado
        try:
            # Cargar la imagen de perfil
            profile_img = Image.open("cinemaster/src/views/images/perfil.png")  # Asegúrate de tener la imagen aquí
            profile_img = profile_img.resize((35, 35))  # Ajustamos el tamaño
            profile_img = ImageTk.PhotoImage(profile_img)
        except:
            profile_img = ImageTk.PhotoImage(Image.open("cinemaster/src/views/images/default.png").resize((35, 35)))  # Si no se encuentra la imagen, usar una predeterminada

        # Botón de perfil con imagen y texto
        self.profile_button = ctk.CTkButton(self.header_frame, text=self.cliente.nombre, font=("Arial", 14),
                                            image=profile_img, compound="left", command=self.redirect_to_profile)
        self.profile_button.image = profile_img  # Mantener la referencia de la imagen
        self.profile_button.pack(side="right", padx=10)

        # Crear un contenedor para los carteles
        self.cartelera_frame = ctk.CTkFrame(self, corner_radius=10)
        self.cartelera_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Obtener las películas desde la base de datos
        self.db_session = next(get_db())
        peliculas = get_all_movies(self.db_session)

        self.carteles = []
        for i, pelicula in enumerate(peliculas):
            pelicula_frame = ctk.CTkFrame(self.cartelera_frame, corner_radius=10, width=180, height=250)
            pelicula_frame.grid(row=0, column=i, padx=20)

            # Obtener la ruta de la imagen de la película desde la base de datos
            image_path = pelicula.Image_path if pelicula.Image_path else os.path.abspath("cinemaster/src/views/images/default.jpg")
            
            try:
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((160, 160), Image.Resampling.LANCZOS)
                self.img = ImageTk.PhotoImage(pil_image)
            except:
                self.img = ImageTk.PhotoImage(Image.open("cinemaster/src/views/images/default.jpg").resize((160, 160)))

            # Imagen de la película
            image_label = ctk.CTkLabel(pelicula_frame, image=self.img, text="")
            image_label.image = self.img  # Aseguramos que la imagen persista
            image_label.pack(pady=10)

            # Información de la película
            info_label = ctk.CTkLabel(pelicula_frame, text=f"Nombre: {pelicula.Title}\nGénero: {pelicula.Gender}\nDuración: {pelicula.Duration} min",
                                      text_color="white", font=("Arial", 12), wraplength=160)
            info_label.pack(pady=5)

            # Obtener los horarios con sus respectivos IDs desde la base de datos
            showtimes_with_ids = [(h.id, h.fecha) for h in pelicula.horarios]
            showtimes_with_ids.sort(key=lambda x: x[1])  # Ordenar por la fecha

            # Mostrar horarios en el dropdown
            showtimes_strings = [f"{showtime[1].strftime('%Y-%m-%d %H:%M')} - ID: {showtime[0]}" for showtime in showtimes_with_ids]

            # Botón de reserva
            reserve_button = ctk.CTkButton(pelicula_frame, text="Reservar", command=lambda pt=pelicula.Title, pd=pelicula.Duration, pg=pelicula.Gender, pi=image_path, showtimes_with_ids=showtimes_with_ids, cliente=self.cliente: self.reserve_movie(pt,pd,pg,pi,showtimes_with_ids, cliente))
            reserve_button.pack(pady=10)

            self.carteles.append(pelicula_frame)

    def redirect_to_profile(self):
        """Función para redirigir al perfil del cliente cuando hace clic en el botón"""
        print("Tipo de self.cliente en redirect_to_profile:", type(self.cliente))
        print("Métodos disponibles en self.cliente:", dir(self.cliente))

        self.destroy()  # Cierra la ventana actual
        from views.profile_view import ProfileView  # Importamos la vista del perfil
        profile_view = ProfileView(self.cliente)  # Pasamos el cliente logueado
        profile_view.mainloop()  # Iniciamos la ventana del perfil

    def reserve_movie(self, pt, pd, pg, pi, showtimes_with_ids, cliente):
        # Llamamos a la vista de reserva, pasando la información de la película y cerrando la cartelera
        self.destroy()  # Cierra la ventana de la cartelera
        open_reservation_view(pt, pd, pg, pi, showtimes_with_ids, cliente)  # Abrir ReservationView con todos los datos de la película seleccionada
