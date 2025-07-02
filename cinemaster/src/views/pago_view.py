import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import requests  # Nueva importación para hacer peticiones HTTP

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
        """Confirma el pago enviando los datos al endpoint de la API"""
        try:
            # Formatear la fecha y hora
            showtime_str = (
                self.selected_showtime_string.strftime('%Y-%m-%d %H:%M')
                if hasattr(self.selected_showtime_string, "strftime")
                else str(self.selected_showtime_string)
            )
            
            # Debug: Imprimir atributos del cliente para verificar
            print(f"🔍 Tipo de cliente: {type(self.cliente)}")
            print(f"🔍 Atributos del cliente: {[attr for attr in dir(self.cliente) if not attr.startswith('_')]}")
            
            # Intentar diferentes posibles nombres de atributos
            client_id = None
            cliente_nombre = None
            cliente_email = None
            
            # Posibles nombres para ID del cliente
            for attr in ['id_cliente', 'client_id', 'id', 'ID', 'cliente_id', 'user_id']:
                if hasattr(self.cliente, attr):
                    client_id = getattr(self.cliente, attr)
                    print(f"✅ Encontrado ID del cliente: {attr} = {client_id}")
                    break
            
            # Posibles nombres para nombre del cliente
            for attr in ['Name', 'name', 'nombre', 'cliente_name', 'username', 'full_name']:
                if hasattr(self.cliente, attr):
                    cliente_nombre = getattr(self.cliente, attr)
                    print(f"✅ Encontrado nombre del cliente: {attr} = {cliente_nombre}")
                    break
            
            # Posibles nombres para email del cliente
            for attr in ['Email', 'email', 'correo', 'mail', 'e_mail']:
                if hasattr(self.cliente, attr):
                    cliente_email = getattr(self.cliente, attr)
                    print(f"✅ Encontrado email del cliente: {attr} = {cliente_email}")
                    break
            
            # Verificar que tenemos los datos mínimos
            if client_id is None:
                # Intentar con valores por defecto o buscar en el objeto
                if hasattr(self.cliente, '__dict__'):
                    print(f"🔍 Contenido del cliente: {self.cliente.__dict__}")
                raise ValueError("No se pudo encontrar el ID del cliente. Atributos disponibles: " + 
                               str([attr for attr in dir(self.cliente) if not attr.startswith('_')]))
            
            if cliente_nombre is None:
                cliente_nombre = "Cliente Sin Nombre"  # Valor por defecto
                print("⚠️ Usando nombre por defecto")
            
            if cliente_email is None:
                cliente_email = "sin-email@ejemplo.com"  # Valor por defecto
                print("⚠️ Usando email por defecto")
            
            # Preparar los datos para el endpoint
            reserva_data = {
                "client_id": int(client_id),  # Asegurar que sea entero
                "id_funcion": int(self.selected_showtime),  # Asegurar que sea entero
                "seat_id": str(self.selected_seat),
                "movie_name": str(self.movie_name),
                "showtime_string": showtime_str,
                "imagen": str(self.movie_image_path) if self.movie_image_path else None,
                "cliente_nombre": str(cliente_nombre),
                "costo_entrada": 12.0,
                "metodo_pago": "tarjeta",
                "cliente_email": str(cliente_email)
            }
            
            print("📤 Enviando datos de reserva a la API...")
            print(f"Datos finales: {reserva_data}")
            
            # Deshabilitar el botón mientras se procesa
            self.confirmar_button.configure(state="disabled", text="Procesando...")
            
            # Llamar al endpoint de la API
            response = requests.post(
                "http://127.0.0.1:8000/reservas/confirmar",
                json=reserva_data,
                timeout=60  # Timeout de 60 segundos
            )
            
            print(f"📥 Respuesta de la API: Status {response.status_code}")
            
            if response.status_code == 200:
                resultado = response.json()
                print(f"📥 Resultado: {resultado}")
                
                if resultado["success"]:
                    messagebox.showinfo(
                        "¡Reserva Confirmada!", 
                        f"✅ {resultado['message']}\n\n"
                        f"🎫 ID de Reserva: {resultado.get('reserva_id', 'N/A')}\n"
                        f"🎬 Película: {self.movie_name}\n"
                        f"💺 Asiento: {self.selected_seat}\n"
                        f"📅 Horario: {showtime_str}"
                    )
                    self.destroy()
                    # Regresar a la cartelera
                    self.regresar_a_cartelera()
                else:
                    messagebox.showerror("Error en la Reserva", resultado["message"])
                    self.confirmar_button.configure(state="normal", text="Confirmar Pago")
            else:
                error_detail = "Error desconocido"
                try:
                    error_response = response.json()
                    error_detail = error_response.get("detail", f"Error HTTP {response.status_code}")
                    print(f"❌ Error de la API: {error_response}")
                except:
                    error_detail = f"Error HTTP {response.status_code}"
                    print(f"❌ Error HTTP: {response.status_code}")
                    print(f"❌ Respuesta: {response.text}")
                
                messagebox.showerror("Error en la Reserva", f"❌ {error_detail}")
                self.confirmar_button.configure(state="normal", text="Confirmar Pago")
                
        except ValueError as ve:
            print(f"❌ Error de validación: {ve}")
            messagebox.showerror("Error de Datos", f"❌ {ve}")
            self.confirmar_button.configure(state="normal", text="Confirmar Pago")
        except requests.exceptions.Timeout:
            print("❌ Timeout de conexión")
            messagebox.showerror("Error de Conexión", "⏰ La petición tardó demasiado. Verifica tu conexión.")
            self.confirmar_button.configure(state="normal", text="Confirmar Pago")
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión con la API")
            messagebox.showerror("Error de Conexión", "🔌 No se pudo conectar con la API. Verifica que esté ejecutándose.")
            self.confirmar_button.configure(state="normal", text="Confirmar Pago")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print(f"❌ Tipo de error: {type(e)}")
            messagebox.showerror("Error", f"❌ Ocurrió un error inesperado: {e}")
            self.confirmar_button.configure(state="normal", text="Confirmar Pago")

    def regresar_a_cartelera(self):
        """Regresa a la vista principal de cartelera"""
        try:
            from views.cartelera_view import MainView
            app = MainView(self.cliente)
            app.mainloop()
        except Exception as e:
            print(f"Error al regresar a cartelera: {e}")