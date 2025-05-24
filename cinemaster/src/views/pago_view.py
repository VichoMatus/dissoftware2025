import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from sqlalchemy.orm import Session
from models.database import get_db, Reserva

from src.services.email_observer import EmailSenderObserver

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

class PagoView(ctk.CTkToplevel):
    def __init__(self, selected_seat, selected_showtime, selected_showtime_string, movie_name, movie_image_path, cliente,
                 booking_facade):
        super().__init__()
        self.title("Sistema de Pagos")
        self.geometry("1280x720")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Datos recibidos
        self.selected_seat = selected_seat
        self.selected_showtime = selected_showtime
        self.selected_showtime_string = selected_showtime_string
        self.movie_name = movie_name
        self.movie_image_path = movie_image_path
        self.cliente = cliente  # Objeto cliente (debe tener cliente_id, nombre, etc.)

        # Controladores
        self.booking_facade = booking_facade

        self.crear_ui()

    def crear_ui(self):
        # Header Frame
        self.frame_header = ctk.CTkFrame(self, height=60)
        self.frame_header.pack(side="top", fill="x")

        # Cargar logo
        current_dir = os.path.dirname(__file__)
        logo_path = os.path.join(current_dir, "images", "logo.png")

        try:
            self.logo_image = Image.open(logo_path)
            self.logo_image = self.logo_image.resize((80, 80))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = ctk.CTkLabel(self.frame_header, image=self.logo_photo, text="")
        except:
            self.logo_label = ctk.CTkLabel(self.frame_header, text="[Logo]")

        self.logo_label.pack(side="left", padx=10)
        ctk.CTkLabel(self.frame_header, text="Sistema de Pagos", font=("Arial", 20, "bold")).pack(side="left", padx=10)

        # Frame principal dividido en dos partes con expansión proporcional
        self.frame_left = ctk.CTkFrame(self)
        self.frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.frame_right = ctk.CTkFrame(self)
        self.frame_right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Contenido Frame Izquierda (Detalles de la Película)
        self.frame_left_content = ctk.CTkFrame(self.frame_left)
        self.frame_left_content.pack(pady=10, padx=10, expand=True, fill="both")

        # Cargar y mostrar la imagen de la película
        self.load_movie_image(self.movie_image_path)

        ctk.CTkLabel(self.frame_left_content, text="Nombre de la Película", font=("Arial", 16, "bold")).pack(pady=5)
        ctk.CTkLabel(self.frame_left_content, text=self.movie_name, font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(self.frame_left_content, text=f"Fecha y Hora: {self.selected_showtime_string}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(self.frame_left_content, text=f"Asiento: {self.selected_seat}", font=("Arial", 14)).pack(pady=5)

        # Contenido Frame Derecha (Pago)
        self.frame_right_content = ctk.CTkFrame(self.frame_right)
        self.frame_right_content.pack(pady=10, padx=10, expand=True, fill="both")

        ctk.CTkLabel(self.frame_right_content, text="Precio del Asiento", font=("Arial", 16, "bold")).pack(pady=5)
        ctk.CTkLabel(self.frame_right_content, text="$12.00", font=("Arial", 14)).pack(pady=10)

        # Botón Confirmar Pago
        ctk.CTkButton(self.frame_right_content, text="Confirmar Pago", font=("Arial", 14), command=self.confirmar_pago).pack(pady=10)

    def load_movie_image(self, image_path):
        try:
            movie_image = Image.open(image_path)
            movie_image = movie_image.resize((500, 400))
            self.movie_image_tk = ImageTk.PhotoImage(movie_image)

            self.movie_image_label = ctk.CTkLabel(self.frame_left_content, image=self.movie_image_tk, text="")
            self.movie_image_label.pack(pady=20)

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            print("Intentando cargar imagen desde:", image_path)

    def confirmar_pago(self):
        try:
            cliente_id = self.cliente.cliente_id
            cliente_name = self.cliente.nombre

            # Registrar observador para envío automático de email
            email_observer = EmailSenderObserver()
            self.booking_facade.register_observer(email_observer)

            reserva = self.booking_facade.book_ticket(
                reservation_data={
                    "client_id": cliente_id,
                    "id_funcion": self.selected_showtime,
                    "seat_id": self.selected_seat
                },
                payment_data={
                    "Costo entrada": 12.0,
                    "Metodo de pago": "tarjeta"
                },
                receipt_data={
                    "movie_name": self.movie_name,
                    "showtime_string": self.selected_showtime_string,
                    "seat": self.selected_seat,
                    "imagen": self.movie_image_path,
                    "cliente_nombre": cliente_name
                }
            )

            messagebox.showinfo(
                "Reserva Confirmada",
                f"Reserva guardada con id: {reserva.reservation_id}\nPago completado con éxito."
            )
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante el pago: {e}")
