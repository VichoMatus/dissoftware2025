import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import os

class PagoView(ctk.CTk):
    def __init__(self, selected_seat, selected_showtime, selected_showtime_string, movie_name, movie_image_path):
        super().__init__()
        self.title("Sistema de Pagos")
        self.geometry("1280x720")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Almacenamos los datos recibidos
        self.selected_seat = selected_seat
        self.selected_showtime = selected_showtime
        self.selected_showtime_string = selected_showtime_string
        self.movie_name = movie_name
        self.movie_image_path = movie_image_path

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

        ctk.CTkLabel(self.frame_left_content, text="Nombre de la Película", font=("Arial", 16, "bold")).pack(pady=5)
        ctk.CTkLabel(self.frame_left_content, text=self.movie_name, font=("Arial", 14)).pack(pady=5)
        
        # Ajustar fecha y hora
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")  # Formato de fecha y hora
        ctk.CTkLabel(self.frame_left_content, text=f"Fecha y Hora: {self.selected_showtime_string}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(self.frame_left_content, text=f"Asiento: {self.selected_seat}", font=("Arial", 14)).pack(pady=5)

        # Mostrar imagen de la película
        try:
            self.movie_image = Image.open(self.movie_image_path)
            self.movie_image = self.movie_image.resize((300, 450))  # Ajustar tamaño de la imagen
            self.movie_photo = ImageTk.PhotoImage(self.movie_image)
            self.movie_image_label = ctk.CTkLabel(self.frame_left_content, image=self.movie_photo, text="")
            self.movie_image_label.pack(pady=10, expand=True, fill="both")
        except:
            ctk.CTkLabel(self.frame_left_content, text="[Imagen de Película]").pack(pady=10)

        # Contenido Frame Derecha (Pago)
        self.frame_right_content = ctk.CTkFrame(self.frame_right)
        self.frame_right_content.pack(pady=10, padx=10, expand=True, fill="both")

        ctk.CTkLabel(self.frame_right_content, text="Precio del Asiento", font=("Arial", 16, "bold")).pack(pady=5)
        ctk.CTkLabel(self.frame_right_content, text="$12.00", font=("Arial", 14)).pack(pady=10)

        # Botón Confirmar Pago
        ctk.CTkButton(self.frame_right_content, text="Confirmar Reserva", font=("Arial", 14), command=self.confirmar_pago).pack(pady=10)

    def confirmar_pago(self):
        # Usar messagebox para mostrar el mensaje de confirmación
        messagebox.showinfo("Reserva Confirmada", "La reserva ha sido confirmada. Puedes revisarla en tu historial de reservas.")