from .command import Command
from api.builders.document_builder import quick_build_ticket
from api.builders.document_processor import get_document_processor
from typing import Dict, Any, Optional

class GenerateReceiptCommand(Command):
    """
    Comando para generar boletas PDF usando el patrón Builder.
    Utiliza el sistema global de Builder + Processor para crear documentos.
    """
    
    def __init__(self, movie_name: str, showtime: str, seat: str, client_name: str, 
                 imagen: Optional[str] = None, ticket_price: float = 12.0):
        self.movie_name = movie_name
        self.showtime = showtime
        self.seat = seat
        self.client_name = client_name
        self.imagen = imagen
        self.ticket_price = ticket_price
    
    def execute(self) -> Dict[str, Any]:
        """
        Ejecuta la generación de boleta PDF usando el patrón Builder.
        
        Returns:
            Dict con el resultado de la generación
        """
        try:
            print(f"🎫 Ejecutando GenerateReceiptCommand usando Builder para {self.client_name}")
            
            # 1. Usar el Builder para construir el documento
            document = quick_build_ticket(
                movie_name=self.movie_name,
                showtime=self.showtime,
                seat=self.seat,
                client_name=self.client_name,
                image_path=self.imagen,
                ticket_price=self.ticket_price
            )
            
            print(f"📄 Documento construido: {document}")
            
            # 2. Usar el Processor para generar el PDF
            processor = get_document_processor()
            resultado = processor.process_to_pdf(document)
            
            if resultado["success"]:
                print(f"✅ Boleta PDF generada exitosamente: {resultado['filename']}")
                print(f"📁 Ruta: {resultado['pdf_path']}")
                
                # Opcional: También generar JSON para debugging/backup
                json_result = processor.process_to_json(document)
                if json_result["success"]:
                    print(f"📋 JSON backup generado: {json_result['filename']}")
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