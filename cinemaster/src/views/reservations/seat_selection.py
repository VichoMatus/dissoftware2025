import customtkinter as ctk
from tkinter import messagebox
import sys
import os
from sqlalchemy.orm import sessionmaker
from models.database import get_db, HorarioAsientos
from PIL import Image, ImageTk

# Importa la clase PagoView desde el archivo pago_view.py
from views.pago_view import PagoView

class SeatSelectionView(ctk.CTk):
    def __init__(self, selected_showtime_id, selected_showtime_string):
        super().__init__()

        self.title("Selección de Asientos")
        self.geometry("1280x720")

        # Configurar el modo oscuro
        ctk.set_appearance_mode("dark")

        # Asignar los parámetros a los atributos de la clase
        self.selected_showtime = selected_showtime_id  # Asigna el ID del horario
        self.selected_showtime_string = selected_showtime_string  # Asigna la cadena con el horario

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

        # Consultar los asientos disponibles para el horario seleccionado
        horario_asientos = self.db_session.query(HorarioAsientos).filter(HorarioAsientos.horario_id == showtime_id).all()

        # Iterar sobre los asientos relacionados con el horario
        for ha in horario_asientos:
            # Acceder al asiento directamente a través de la relación de SQLAlchemy
            asiento = ha.asiento  # Esto se asume si tienes la relación correctamente definida
            if asiento:  # Verificamos si el asiento existe
                available_seats.append(asiento.ids_seats)

        return available_seats

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
            
            # Obtener el nombre de la película y la ruta de la imagen (esto lo deberías obtener de tu base de datos o lógica)
            movie_name = "La Era del Hielo 5"  # Este valor debería ser dinámico basado en la selección
            movie_image_path = "cinemaster/src/views/images/La_Era_del_Hielo_5.jpg"  # Ruta a la imagen de la película
            
            # Pasamos los datos seleccionados a la vista de pago
            self.open_payment_view(selected_seat, self.selected_showtime, self.selected_showtime_string, movie_name, movie_image_path)
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado un asiento.")

    def open_payment_view(self, selected_seat, selected_showtime, selected_showtime_string, movie_name, movie_image_path):
        # Abrir la vista de pago y pasarle los datos seleccionados
        payment_view = PagoView(selected_seat, selected_showtime, selected_showtime_string, movie_name, movie_image_path)  
        payment_view.mainloop()  # Ejecutar el mainloop de la interfaz de pago


# Esta función se encargará de abrir la ventana de selección de asientos
def open_seat_selection_view(selected_showtime_id, selected_showtime_string):
    seat_selection_app = SeatSelectionView(selected_showtime_id, selected_showtime_string)
    seat_selection_app.mainloop()