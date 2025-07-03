import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from typing import Optional

class BoletaService:
    """
    Servicio para generar boletas PDF a través de la API.
    Separado de la lógica de reservas para mantener responsabilidades claras.
    """
    
    def __init__(self):
        self.boletas_dir = os.path.abspath("Boletas")
        self.logo_path = os.path.abspath("cinemaster/src/views/images/logo.png")
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Crea el directorio de boletas si no existe"""
        if not os.path.exists(self.boletas_dir):
            os.makedirs(self.boletas_dir)
            print(f"📁 Directorio creado: {self.boletas_dir}")
    
    def generar_boleta_para_reserva(self, movie_name: str, showtime: str, seat: str, 
                                   client_name: str, imagen: Optional[str] = None) -> dict:
        """
        Genera una boleta PDF para una reserva específica.
        
        Args:
            movie_name: Nombre de la película
            showtime: Horario de la función
            seat: Asiento reservado
            client_name: Nombre del cliente
            imagen: Ruta opcional de la imagen de la película
            
        Returns:
            dict: Resultado de la operación con éxito/error y ruta del archivo
        """
        try:
            # Generar nombre del archivo con formato: boleta_{client_name}_{movie_name}.pdf
            filename = f"boleta_{client_name}_{movie_name}.pdf"
            # Limpiar caracteres especiales del filename
            filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
            pdf_path = os.path.join(self.boletas_dir, filename)
            
            # Generar el PDF
            success = self._crear_boleta_pdf(
                pdf_path=pdf_path,
                movie_name=movie_name,
                showtime=showtime,
                seat=seat,
                client_name=client_name,
                imagen=imagen
            )
            
            if success:
                return {
                    "success": True,
                    "message": f"Boleta generada exitosamente para {client_name}",
                    "pdf_path": pdf_path,
                    "filename": filename
                }
            else:
                return {
                    "success": False,
                    "message": "Error al generar el archivo PDF",
                    "pdf_path": None,
                    "filename": None
                }
                
        except Exception as e:
            print(f"❌ Error generando boleta: {e}")
            return {
                "success": False,
                "message": f"Error interno al generar la boleta: {str(e)}",
                "pdf_path": None,
                "filename": None
            }
    
    def _crear_boleta_pdf(self, pdf_path: str, movie_name: str, showtime: str, 
                         seat: str, client_name: str, imagen: Optional[str] = None) -> bool:
        """
        Crea un PDF de boleta usando ReportLab.
        Función privada basada en generarBoleta.py pero adaptada para la API.
        """
        try:
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            c = canvas.Canvas(pdf_path, pagesize=A4)
            
            # Logo de CineMaster
            try:
                logo = ImageReader(self.logo_path)
                c.drawImage(logo, x=400, y=700, width=150, height=150, mask='auto')
            except Exception as e:
                print(f"No se pudo cargar el logo: {e}")
            
            # Título principal
            c.setFont("Helvetica-Bold", 16)
            c.drawString(240, 800, "Boleta CineMaster")
            
            # Información de la reserva
            c.setFont("Helvetica", 12)
            c.drawString(50, 780, f"Película: {movie_name}")
            c.drawString(50, 760, f"Cliente: {client_name}")
            c.drawString(50, 740, f"Fecha y hora de función: {showtime}")
            c.drawString(50, 720, f"Asiento: {seat}")
            c.drawString(50, 700, f"Boleta generada el: {fecha_actual}")
            
            # Imagen de la película (si está disponible)
            if imagen and os.path.exists(imagen):
                try:
                    pelicula_img = ImageReader(imagen)
                    c.drawImage(pelicula_img, x=50, y=400, width=500, height=300, mask='auto')
                except Exception as e:
                    print(f"No se pudo cargar la imagen de la película: {e}")
            
            # Información de contacto
            c.drawString(50, 380, "Gracias por su compra. Para consultas llame al +56 9 6969 6969.")
            c.drawString(50, 365, "O contactarnos por correo: cinemaster2006@gmail.com")
            
            # Línea decorativa
            c.line(50, 350, 550, 350)
            
            # Código de barras simulado
            c.setFont("Helvetica", 8)
            c.drawString(50, 330, f"Código de reserva: CM-{datetime.now().strftime('%Y%m%d%H%M%S')}")
            
            c.save()
            print(f"📄 PDF guardado en: {pdf_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error generando PDF: {e}")
            return False

# Instancia global del servicio para usar en endpoints
boleta_service = BoletaService()