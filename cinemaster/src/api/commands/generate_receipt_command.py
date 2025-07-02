from .command import Command
from api.services.boleta_service import boleta_service
from typing import Dict, Any, Optional

class GenerateReceiptCommand(Command):
    """
    Comando para generar boletas PDF en la API.
    Utiliza el servicio de boletas para crear el archivo.
    """
    
    def __init__(self, movie_name: str, showtime: str, seat: str, client_name: str, imagen: Optional[str] = None):
        self.movie_name = movie_name
        self.showtime = showtime
        self.seat = seat
        self.client_name = client_name
        self.imagen = imagen
    
    def execute(self) -> Dict[str, Any]:
        """
        Ejecuta la generación de boleta PDF.
        
        Returns:
            Dict con el resultado de la generación
        """
        try:
            print(f"🎫 Ejecutando GenerateReceiptCommand para {self.client_name}")
            
            # Usar el servicio de boletas para generar el PDF
            resultado = boleta_service.generar_boleta_para_reserva(
                movie_name=self.movie_name,
                showtime=self.showtime,
                seat=self.seat,
                client_name=self.client_name,
                imagen=self.imagen
            )
            
            if resultado["success"]:
                print(f"✅ Boleta generada exitosamente: {resultado['filename']}")
            else:
                print(f"❌ Error generando boleta: {resultado['message']}")
            
            return resultado
            
        except Exception as e:
            print(f"❌ Error en GenerateReceiptCommand: {e}")
            return {
                "success": False,
                "message": f"Error interno al generar la boleta: {str(e)}",
                "pdf_path": None,
                "filename": None
            }