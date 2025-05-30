import customtkinter as ctk
from tkinter import messagebox
import sys
import os
from sqlalchemy.orm import sessionmaker
from models.database import get_db, HorarioAsientos
from PIL import Image, ImageTk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
# Importa la clase PagoView desde el archivo pago_view.py
from views.pago_view import PagoView

class SeatSelectionView(ctk.CTkToplevel):
    def __init__(self, selected_showtime_id, selected_showtime_string, movie_name, movie_image_path, cliente, booking_facade):
        super().__init__()

        self.title("Selección de Asientos")
        self.geometry("1280x720")

        # Configurar el modo oscuro
        ctk.set_appearance_mode("dark")

        # Asignar los parámetros a los atributos de la clase
        self.selected_showtime = selected_showtime_id  # Asigna el ID del horario
        self.selected_showtime_string = selected_showtime_string  # Asigna la cadena con el horario
        self.movie_image_path = movie_image_path
        self.movie_name = movie_name
        self.cliente = cliente

        # Controladores
        self.booking_facade = booking_facade

        # Obtener la base de datos y la sesión
        self.db_session = next(get_db())

        # Obtener los asientos disponibles para el horario seleccionado
        self.selected_showtime_id = selected_showtime_id
        self.selected_showtime_string = selected_showtime_string

        # Obtener los asientos disponibles desde la base de datos
        self.seat_options = self.get_available_seats(selected_showtime_id)

        # Crear los frames
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill='x', padx=20, pady=10)

        # Frame para contener la imagen a la izquierda y la selección de asientos a la derecha
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Crear los frames para la imagen y la selección de asientos
        self.image_frame = ctk.CTkFrame(self.main_frame)
        self.image_frame.pack(side="left", padx=10, pady=15)

        self.selection_frame = ctk.CTkFrame(self.main_frame)
        self.selection_frame.pack(side="right", padx=10, fill="both", expand=True)
        # Header con el logo
        self.create_header()

        self.encabezado_label = ctk.CTkLabel(self.selection_frame, text="Selección de Asientos", font=("Arial", 20))
        self.encabezado_label.pack(pady=20)
        
        # Mostrar el horario de la película seleccionada
        self.showtime_label = ctk.CTkLabel(self.selection_frame, text=f"Horario: {selected_showtime_string}", font=("Arial", 14))
        self.showtime_label.pack(pady=10)

        # Mostrar el dropdown para seleccionar el asiento
        self.show_seat_dropdown()

        # Cargar y mostrar la imagen
        image_path = os.path.abspath("cinemaster/src/views/images/Asientos.png")
        self.load_seat_image(image_path)

        # Botón para confirmar la selección
        self.confirm_button = ctk.CTkButton(self.selection_frame, text="Confirmar Selección", width=200, height=40, command=self.confirm_selection)
        self.confirm_button.pack(pady=30)

    def create_header(self):
        # Frame para el header
        current_dir = os.path.dirname(__file__)
        logo_path = os.path.join(current_dir, "..", "images", "logo.png")

        self.logo_image = Image.open(logo_path)
        self.logo_image = self.logo_image.resize((100, 100))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = ctk.CTkLabel(self.header_frame, image=self.logo_photo, text="")
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

    def load_seat_image(self, image_path):
        # Asegurarnos de que la ruta de la imagen sea válida
        try:
            # Cargar y redimensionar la imagen
            seat_image = Image.open(image_path)
            seat_image = seat_image.resize((500, 400))  # Redimensionar la imagen a 500x400
            seat_image_tk = ImageTk.PhotoImage(seat_image)

            # Crear un widget CTkLabel con la imagen
            self.seat_image_label = ctk.CTkLabel(self.image_frame, image=seat_image_tk, text="")
            self.seat_image_label.pack(side="left", padx=100)

            # Mantener una referencia de la imagen para evitar que se pierda
            self.seat_image_label.image = seat_image_tk

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def get_available_seats(self, showtime_id):
        available_seats = []

        horario_asientos = self.db_session.query(HorarioAsientos)\
            .filter(HorarioAsientos.horario_id == showtime_id, HorarioAsientos.Available == True).all()

        for ha in horario_asientos:
            asiento = ha.asiento
            if asiento:
                available_seats.append(asiento.ids_seats)
        return self.booking_facade.get_available_seats(showtime_id)



    def show_seat_dropdown(self):
        """Crea el OptionMenu para seleccionar el asiento con las opciones disponibles."""
        if self.seat_options:
            self.selected_seat = ctk.StringVar(value=self.seat_options[0])  # Valor por defecto

            self.seat_dropdown = ctk.CTkOptionMenu(self.selection_frame, variable=self.selected_seat, values=self.seat_options)
            self.seat_dropdown.pack(pady=20)  # Mostrar el OptionMenu con los asientos disponibles

    def confirm_selection(self):
        selected_seat = self.selected_seat.get()
        if selected_seat:
            messagebox.showinfo("Selección Confirmada", f"Has seleccionado el asiento: {selected_seat}")            
            # Pasamos los datos seleccionados a la vista de pago
            self.destroy()
            self.open_payment_view(selected_seat, self.selected_showtime, self.selected_showtime_string, self.movie_name, self.movie_image_path, self.cliente)

        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado un asiento.")

    def redirect_to_profile(self):
        """Función para redirigir al perfil del cliente cuando hace clic en el botón"""
        print("Tipo de self.cliente en redirect_to_profile:", type(self.cliente))
        print("Métodos disponibles en self.cliente:", dir(self.cliente))

        self.destroy()  # Cierra la ventana actual
        from views.profile_view import ProfileView  # Importamos la vista del perfil
        profile_view = ProfileView(self.cliente)  # Pasamos el cliente logueado
        profile_view.mainloop()  # Iniciamos la ventana del perfil
        
    def open_payment_view(self, selected_seat, selected_showtime, selected_showtime_string, movie_name, movie_image_path, cliente):
        # Usamos los controladores de esta instancia
        self.pago_view = PagoView(selected_seat, selected_showtime, selected_showtime_string, movie_name, movie_image_path, self.cliente,
                          self.booking_facade)

        self.pago_view.grab_set()  # Opcional para que la ventana sea modal y capture eventos

def open_seat_selection_view(selected_showtime_id, selected_showtime_date, movie_name, movie_image_path,cliente, booking_facade):
    SeatSelectionView(selected_showtime_id, selected_showtime_date, movie_name, movie_image_path, cliente, booking_facade)