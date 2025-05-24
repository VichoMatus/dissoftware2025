import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
from tkinter import messagebox

class generarBoleta:
    def __init__(self, movie_name, showtime, seat, imagen, client_name="Cliente", logo_path=None):
        self.movie_name = movie_name
        self.showtime = showtime
        self.seat = seat if isinstance(seat, list) else [seat]
        self.client_name = client_name
        self.imagen = imagen
        self.logo_path = os.path.abspath("cinemaster/src/views/images/logo.png")

    def crear_pdf(self, ruta_pdf):
        try:
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            c = canvas.Canvas(ruta_pdf, pagesize=A4)

            try:
                logo = ImageReader(self.logo_path)
                c.drawImage(logo, x=400, y=700, width=150, height=150, mask='auto')
            except Exception as e:
                print(f"No se pudo cargar el logo: {e}")

            c.setFont("Helvetica-Bold", 16)
            c.drawString(240, 800, "Boleta CineMaster")
            c.setFont("Helvetica", 12)
            c.drawString(50, 780, f"Película: {self.movie_name}")
            c.drawString(50, 760, f"Cliente: {self.client_name}")
            c.drawString(50, 740, f"Fecha y hora de función: {self.showtime}")
            c.drawString(50, 720, f"Asiento(s): {', '.join(self.seat)}")

            try:
                pelicula_img = ImageReader(self.imagen)
                c.drawImage(pelicula_img, x=50, y=400, width=500, height=300, mask='auto')
            except Exception as e:
                print(f"No se pudo cargar la imagen de la película: {e}")

            c.drawString(50, 380, "Gracias por su compra. Para consultas llame al +56 9 6969 6969.")
            c.drawString(50, 365, "O contactarnos por correo: cinemaster2006@gmail.com")

            c.save()
            print(f"PDF guardado en: {ruta_pdf}")
            messagebox.showinfo("Boleta generada", f"Boleta guardada en: {ruta_pdf}")

        except Exception as e:
            print(f"Error generando PDF: {e}")
            messagebox.showerror("Error", f"No se pudo generar la boleta PDF: {e}")

    def generate_receipt(self, ruta_pdf_completa):
        self.crear_pdf(ruta_pdf_completa)
