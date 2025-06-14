import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from utils.decorators import medir_tiempo
from views.Cartelera_Solid.profile_button import ProfileButton
from controllers.reservation_controller import ReservationController

class ReservationView(ctk.CTkToplevel):
    def __init__(self, selected_movie_Title, selected_movie_Duration, selected_movie_Gender, movie_image_path, showtimes_with_ids, cliente, reservation_system):
        super().__init__()

        self.title("Cine Master")
        self.geometry("1280x720")
        self.resizable(True, True)
        ctk.set_appearance_mode("dark")

        self.cliente = cliente
        self.selected_movie_Title = selected_movie_Title
        self.selected_movie_Duration = selected_movie_Duration
        self.selected_movie_Gender = selected_movie_Gender
        self.movie_image_path = movie_image_path
        self.showtimes_with_ids = showtimes_with_ids

        self.controller = ReservationController(reservation_system)

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill='x', padx=20, pady=10)

        self.reservation_frame = ctk.CTkFrame(self)
        self.reservation_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.create_widgets()

    def load_movie_image(self):
        """Carga y devuelve la imagen de la película redimensionada."""
        image_path = self.movie_image_path if self.movie_image_path and os.path.exists(self.movie_image_path) \
            else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images", "default.jpg"))
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((200, 200))
        return ImageTk.PhotoImage(pil_image)

    def get_selected_showtime(self):
        """Devuelve el ID y la fecha del horario seleccionado."""
        selected_showtime_string = self.selected_showtime.get()
        for showtime in self.showtimes_with_ids:
            showtime_string = f"{showtime[1].strftime('%Y-%m-%d %H:%M')} - ID: {showtime[0]}"
            if selected_showtime_string == showtime_string:
                return showtime[0], showtime[1]
        return None, None

    @medir_tiempo
    def create_widgets(self):
        # Header
        self.app_name_label = ctk.CTkLabel(self.header_frame, text="CineMaster", font=("Arial", 24, "bold"))
        self.app_name_label.pack(side="left", padx=10)
        self.profile_button = ProfileButton(self.header_frame, self.cliente)

        # Imagen de la película
        self.img = self.load_movie_image()
        image_label = ctk.CTkLabel(self.reservation_frame, image=self.img, text="")
        image_label.image = self.img
        image_label.grid(row=0, column=0, padx=20, pady=20, rowspan=4)

        # Info de la película
        info_label = ctk.CTkLabel(
            self.reservation_frame,
            text=f"Título: {self.selected_movie_Title}\nGénero: {self.selected_movie_Gender}\nDuración: {self.selected_movie_Duration} min",
            font=("Arial", 14),
            justify="left"
        )
        info_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        # Selección de horario
        self.showtimes_label = ctk.CTkLabel(self.reservation_frame, text="Horarios disponibles:")
        self.showtimes_label.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        self.showtimes_strings = [f"{showtime[1].strftime('%Y-%m-%d %H:%M')} - ID: {showtime[0]}" for showtime in self.showtimes_with_ids]
        self.selected_showtime = ctk.StringVar(value=self.showtimes_strings[0])
        self.showtime_dropdown = ctk.CTkOptionMenu(self.reservation_frame, variable=self.selected_showtime, values=self.showtimes_strings)
        self.showtime_dropdown.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.reserve_button = ctk.CTkButton(self.reservation_frame, text="Continuar a selección de asiento", width=200, height=40, command=self.reserve_movie)
        self.reserve_button.grid(row=3, column=1, padx=20, pady=20, sticky="w")

    def reserve_movie(self):
        selected_showtime_id, selected_showtime_date = self.get_selected_showtime()
        if selected_showtime_id is None:
            messagebox.showerror("Error", "No se ha seleccionado un horario válido.")
            return

        messagebox.showinfo("Reserva", f"Selecciona tu asiento para la película: {self.selected_movie_Title}\nHorario: {selected_showtime_date.strftime('%Y-%m-%d %H:%M')}")
        self.destroy()
        from views.reservations.seat_selection import open_seat_selection_view
        open_seat_selection_view(selected_showtime_id, selected_showtime_date, self.selected_movie_Title, self.movie_image_path, self.cliente, self.controller.reservation_system)

def open_reservation_view(selected_movie_Title, selected_movie_Duration, selected_movie_Gender, movie_image_path, showtimes_with_ids, cliente, reservation_system):
    ReservationView(selected_movie_Title, selected_movie_Duration, selected_movie_Gender, movie_image_path, showtimes_with_ids, cliente, reservation_system)