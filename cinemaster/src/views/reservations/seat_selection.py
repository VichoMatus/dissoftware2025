import customtkinter as ctk
from tkinter import messagebox
import sys
import os
from sqlalchemy.orm import sessionmaker
from models.database import get_db, HorarioAsientos
from PIL import Image, ImageTk
from models.profile_button import ProfileButton  # Importar ProfileButton

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from views.pago_view import PagoView

class SeatSelectionView(ctk.CTkToplevel):
    def __init__(self, selected_showtime_id, selected_showtime_string, movie_name, movie_image_path, cliente, booking_facade):
        super().__init__()

        self.title("Selección de Asientos")
        self.geometry("1280x720")

        ctk.set_appearance_mode("dark")

        self.selected_showtime = selected_showtime_id
        self.selected_showtime_string = selected_showtime_string
        self.movie_image_path = movie_image_path
        self.movie_name = movie_name
        self.cliente = cliente

        self.booking_facade = booking_facade

        self.db_session = next(get_db())

        self.seat_options = self.get_available_seats(selected_showtime_id)

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill='x', padx=20, pady=10)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.image_frame = ctk.CTkFrame(self.main_frame)
        self.image_frame.pack(side="left", padx=10, pady=15)

        self.selection_frame = ctk.CTkFrame(self.main_frame)
        self.selection_frame.pack(side="right", padx=10, fill="both", expand=True)

        # Usamos ProfileButton solo una vez aquí
        self.profile_button = ProfileButton(self.header_frame, self.cliente)

        self.create_header()

        self.encabezado_label = ctk.CTkLabel(self.selection_frame, text="Selección de Asientos", font=("Arial", 20))
        self.encabezado_label.pack(pady=20)

        self.showtime_label = ctk.CTkLabel(self.selection_frame, text=f"Horario: {selected_showtime_string}", font=("Arial", 14))
        self.showtime_label.pack(pady=10)

        self.show_seat_dropdown()

        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "views", "images", "Asientos.png"))
        self.load_seat_image(image_path)

        self.confirm_button = ctk.CTkButton(self.selection_frame, text="Confirmar Selección", width=200, height=40, command=self.confirm_selection)
        self.confirm_button.pack(pady=30)

    def create_header(self):
        current_dir = os.path.dirname(__file__)
        logo_path = os.path.join(current_dir, "..", "images", "logo.png")

        self.logo_image = Image.open(logo_path)
        self.logo_image = self.logo_image.resize((100, 100))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = ctk.CTkLabel(self.header_frame, image=self.logo_photo, text="")
        self.logo_label.pack(side="left", padx=10)

        self.app_name_label = ctk.CTkLabel(self.header_frame, text="CineMaster", font=("Arial", 24, "bold"))
        self.app_name_label.pack(side="left", padx=10)

        # Aquí no es necesario crear otro profile_button, ya se agregó en la línea anterior

    def load_seat_image(self, image_path):
        try:
            seat_image = Image.open(image_path)
            seat_image = seat_image.resize((500, 400))
            seat_image_tk = ImageTk.PhotoImage(seat_image)

            self.seat_image_label = ctk.CTkLabel(self.image_frame, image=seat_image_tk, text="")
            self.seat_image_label.pack(side="left", padx=100)

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
        if self.seat_options:
            self.selected_seat = ctk.StringVar(value=self.seat_options[0])
            self.seat_dropdown = ctk.CTkOptionMenu(self.selection_frame, variable=self.selected_seat, values=self.seat_options)
            self.seat_dropdown.pack(pady=20)

    def confirm_selection(self):
        selected_seat = self.selected_seat.get()
        if selected_seat:
            messagebox.showinfo("Selección Confirmada", f"Has seleccionado el asiento: {selected_seat}")            
            self.destroy()
            self.open_payment_view(selected_seat, self.selected_showtime, self.selected_showtime_string, self.movie_name, self.movie_image_path, self.cliente)
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado un asiento.")

    def redirect_to_profile(self):
        self.destroy()
        from views.profile_view import ProfileView
        profile_view = ProfileView(self.cliente)
        profile_view.mainloop()

    def open_payment_view(self, selected_seat, selected_showtime, selected_showtime_string, movie_name, movie_image_path, cliente):
        self.pago_view = PagoView(selected_seat, selected_showtime, selected_showtime_string, movie_name, movie_image_path, self.cliente, self.booking_facade)
        self.pago_view.grab_set()

def open_seat_selection_view(selected_showtime_id, selected_showtime_date, movie_name, movie_image_path, cliente, booking_facade):
    SeatSelectionView(selected_showtime_id, selected_showtime_date, movie_name, movie_image_path, cliente, booking_facade)
