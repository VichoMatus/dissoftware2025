import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os
from services.payment_api_client import confirmar_pago
import webbrowser

class PagoView(ctk.CTkToplevel):
    def __init__(self, selected_seat, selected_showtime, selected_showtime_string, movie_name, movie_image_path, cliente, booking_facade):
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
        self.booking_facade = booking_facade

        self.crear_ui()

    def crear_ui(self):
        # Header
        self.frame_header = ctk.CTkFrame(self)
        self.frame_header.pack(fill='x', padx=20, pady=10)
        self.logo_label = ctk.CTkLabel(self.frame_header, text="🎬", font=("Arial", 32))
        self.logo_label.pack(side="left", padx=10)
        ctk.CTkLabel(self.frame_header, text="Sistema de Pagos", font=("Arial", 20, "bold")).pack(side="left", padx=10)

        # Frame principal dividido en dos partes
        self.frame_left = ctk.CTkFrame(self)
        self.frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.frame_right = ctk.CTkFrame(self)
        self.frame_right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame Izquierda (Detalles de la Película)
        self.frame_left_content = ctk.CTkFrame(self.frame_left)
        self.frame_left_content.pack(pady=10, padx=10, expand=True, fill="both")

        self.load_movie_image(self.movie_image_path)

        ctk.CTkLabel(self.frame_left_content, text="Nombre de la Película", font=("Arial", 16, "bold")).pack(pady=5)
        ctk.CTkLabel(self.frame_left_content, text=self.movie_name, font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(self.frame_left_content, text=f"Fecha y Hora: {self.selected_showtime_string}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(self.frame_left_content, text=f"Asiento: {self.selected_seat}", font=("Arial", 14)).pack(pady=5)

        # Frame Derecha (Pago)
        self.frame_right_content = ctk.CTkFrame(self.frame_right)
        self.frame_right_content.pack(pady=10, padx=10, expand=True, fill="both")

        ctk.CTkLabel(self.frame_right_content, text="Precio del Asiento", font=("Arial", 16, "bold")).pack(pady=5)
        ctk.CTkLabel(self.frame_right_content, text="$12.00", font=("Arial", 14)).pack(pady=10)

        # Botón Confirmar Pago
        self.confirmar_button = ctk.CTkButton(
            self.frame_right_content,
            text="Confirmar Pago",
            command=self.confirmar_pago_btn
        )
        self.confirmar_button.pack(pady=20)

    def load_movie_image(self, image_path):
        try:
            if image_path and os.path.exists(image_path):
                pil_image = Image.open(image_path)
            else:
                # Busca default.jpg en la carpeta images
                default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images", "default.jpg"))
                if os.path.exists(default_path):
                    pil_image = Image.open(default_path)
                else:
                    # Si tampoco existe default.jpg, crea una imagen vacía con texto
                    pil_image = Image.new("RGB", (200, 200), color="gray")
                    draw = ImageDraw.Draw(pil_image)
                    draw.text((50, 90), "Sin imagen", fill="white")
            pil_image = pil_image.resize((200, 200))
            self.img = ImageTk.PhotoImage(pil_image)
            image_label = ctk.CTkLabel(self.frame_left_content, image=self.img, text="")
            image_label.image = self.img
            image_label.pack(pady=10)
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            # Si hay error, muestra solo texto
            ctk.CTkLabel(self.frame_left_content, text="No se pudo cargar la imagen").pack(pady=10)

    def confirmar_pago_btn(self):
        try:
            showtime_str = (
                self.selected_showtime_string.strftime('%Y-%m-%d %H:%M')
                if hasattr(self.selected_showtime_string, "strftime")
                else str(self.selected_showtime_string)
            )
            url = (
                f"http://127.0.0.1:8000/confirmar_pago_web/"
                f"?client_id={self.cliente.cliente_id}"
                f"&id_funcion={self.selected_showtime}"
                f"&seat_id={self.selected_seat}"
                f"&movie_name={self.movie_name}"
                f"&showtime_string={showtime_str}"
                f"&imagen={self.movie_image_path}"
                f"&cliente_nombre={self.cliente.nombre}"
                f"&costo_entrada=12.0"
                f"&metodo_pago=tarjeta"
                f"&cliente_email={self.cliente.Email}" 
            )
            webbrowser.open(url)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al abrir la confirmación: {e}")