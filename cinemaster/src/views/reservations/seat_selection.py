import customtkinter as ctk
from tkinter import messagebox
import sys
import os
import requests  # Nueva importación
from PIL import Image, ImageTk
from views.Cartelera_Solid.profile_button import ProfileButton
from views.reservations.widgets.seat_image_widget import SeatImageWidget

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

        # SOLO API - sin conexión a base de datos
        self.seat_options = self.get_available_seats_from_api(selected_showtime_id)

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill='x', padx=20, pady=10)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.image_frame = ctk.CTkFrame(self.main_frame)
        self.image_frame.pack(side="left", padx=10, pady=15)

        self.selection_frame = ctk.CTkFrame(self.main_frame)
        self.selection_frame.pack(side="right", padx=10, fill="both", expand=True)

        self.profile_button = ProfileButton(self.header_frame, self.cliente)
        self.create_header()

        self.encabezado_label = ctk.CTkLabel(self.selection_frame, text="Selección de Asientos", font=("Arial", 20))
        self.encabezado_label.pack(pady=20)

        self.showtime_label = ctk.CTkLabel(self.selection_frame, text=f"Horario: {selected_showtime_string}", font=("Arial", 14))
        self.showtime_label.pack(pady=10)

        # Crear el botón de confirmación ANTES de show_seat_dropdown
        self.confirm_button = ctk.CTkButton(self.selection_frame, text="Confirmar Selección", width=200, height=40, command=self.confirm_selection)
        self.confirm_button.pack(pady=30)

        self.show_seat_dropdown()

        # Usa el widget para la imagen de asientos
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images", "Asientos.png"))
        self.seat_image_widget = SeatImageWidget(self.image_frame, image_path)
        self.seat_image_widget.pack(side="left", padx=100)

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

    def get_available_seats_from_api(self, showtime_id):
        """Obtiene los asientos disponibles EXCLUSIVAMENTE desde la API"""
        try:
            response = requests.get(f"http://127.0.0.1:8000/cartelera/horarios/{showtime_id}/asientos")
            if response.status_code == 200:
                asientos_data = response.json()
                # Filtrar solo asientos disponibles y usar el campo correcto
                available_seats = []
                for asiento in asientos_data:
                    if asiento.get('disponible', False):  # Solo asientos disponibles
                        available_seats.append(asiento['numero_asiento'])
                return available_seats
            else:
                print(f"❌ Error al obtener asientos desde API: {response.status_code}")
                messagebox.showerror("Error", f"No se pudieron cargar los asientos desde la API. Código: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error conectando con la API para asientos: {e}")
            messagebox.showerror("Error de Conexión", "No se pudo conectar con la API para obtener los asientos.")
            return []

    def show_seat_dropdown(self):
        if self.seat_options:
            self.selected_seat = ctk.StringVar(value=self.seat_options[0])
            self.seat_dropdown = ctk.CTkOptionMenu(self.selection_frame, variable=self.selected_seat, values=self.seat_options)
            self.seat_dropdown.pack(pady=20)
        else:
            # Si no hay asientos disponibles desde la API
            self.no_seats_label = ctk.CTkLabel(self.selection_frame, text="❌ No hay asientos disponibles", font=("Arial", 16), text_color="red")
            self.no_seats_label.pack(pady=20)
            self.confirm_button.configure(state="disabled")

    def confirm_selection(self):
        if hasattr(self, 'selected_seat') and self.selected_seat:
            selected_seat = self.selected_seat.get()
            if selected_seat:
                messagebox.showinfo("Selección Confirmada", f"Has seleccionado el asiento: {selected_seat}")            
                self.destroy()
                self.open_payment_view(selected_seat, self.selected_showtime, self.selected_showtime_string, self.movie_name, self.movie_image_path, self.cliente)
            else:
                messagebox.showwarning("Advertencia", "No se ha seleccionado un asiento.")
        else:
            messagebox.showwarning("Advertencia", "No hay asientos disponibles para seleccionar.")

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