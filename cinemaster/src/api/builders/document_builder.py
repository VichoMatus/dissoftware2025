"""
Patrón Builder Global para generar documentos (boletos, reportes, facturas, etc.)
Este patrón permite construir objetos complejos paso a paso de manera flexible.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid


class Document:
    """
    Producto final del Builder - Representa un documento genérico
    """
    def __init__(self):
        self.document_type: str = ""
        self.document_id: str = str(uuid.uuid4())
        self.timestamp: datetime = datetime.now()
        self.title: str = ""
        self.subtitle: str = ""
        self.content: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
        self.styling: Dict[str, Any] = {}
        self.footer: str = ""
        self.header: str = ""
        self.attachments: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el documento a diccionario para fácil serialización"""
        return {
            "document_type": self.document_type,
            "document_id": self.document_id,
            "timestamp": self.timestamp.isoformat(),
            "title": self.title,
            "subtitle": self.subtitle,
            "content": self.content,
            "metadata": self.metadata,
            "styling": self.styling,
            "header": self.header,
            "footer": self.footer,
            "attachments": self.attachments
        }
    
    def __str__(self) -> str:
        return f"Document(type={self.document_type}, id={self.document_id[:8]}...)"


class DocumentBuilder(ABC):
    """
    Interfaz abstracta para constructores de documentos
    """
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        """Reinicia el builder para crear un nuevo documento"""
        self._document = Document()
    
    @property
    def document(self) -> Document:
        """Retorna el documento construido y reinicia el builder"""
        result = self._document
        self.reset()
        return result
    
    @abstractmethod
    def set_document_type(self, doc_type: str) -> 'DocumentBuilder':
        pass
    
    @abstractmethod
    def set_title(self, title: str) -> 'DocumentBuilder':
        pass
    
    @abstractmethod
    def set_subtitle(self, subtitle: str) -> 'DocumentBuilder':
        pass
    
    @abstractmethod
    def add_content(self, key: str, value: Any) -> 'DocumentBuilder':
        pass
    
    @abstractmethod
    def set_metadata(self, key: str, value: Any) -> 'DocumentBuilder':
        pass
    
    @abstractmethod
    def set_styling(self, key: str, value: Any) -> 'DocumentBuilder':
        pass


class ConcreteDocumentBuilder(DocumentBuilder):
    """
    Constructor concreto que implementa todos los métodos del builder
    """
    
    def set_document_type(self, doc_type: str) -> 'ConcreteDocumentBuilder':
        """Establece el tipo de documento (boleto, factura, reporte, etc.)"""
        self._document.document_type = doc_type
        return self
    
    def set_title(self, title: str) -> 'ConcreteDocumentBuilder':
        """Establece el título principal del documento"""
        self._document.title = title
        return self
    
    def set_subtitle(self, subtitle: str) -> 'ConcreteDocumentBuilder':
        """Establece el subtítulo del documento"""
        self._document.subtitle = subtitle
        return self
    
    def add_content(self, key: str, value: Any) -> 'ConcreteDocumentBuilder':
        """Añade contenido al documento"""
        self._document.content[key] = value
        return self
    
    def set_metadata(self, key: str, value: Any) -> 'ConcreteDocumentBuilder':
        """Añade metadatos al documento"""
        self._document.metadata[key] = value
        return self
    
    def set_styling(self, key: str, value: Any) -> 'ConcreteDocumentBuilder':
        """Configura el estilo del documento"""
        self._document.styling[key] = value
        return self
    
    def set_header(self, header: str) -> 'ConcreteDocumentBuilder':
        """Establece el encabezado del documento"""
        self._document.header = header
        return self
    
    def set_footer(self, footer: str) -> 'ConcreteDocumentBuilder':
        """Establece el pie de página del documento"""
        self._document.footer = footer
        return self
    
    def add_attachment(self, attachment_path: str) -> 'ConcreteDocumentBuilder':
        """Añade un adjunto al documento"""
        self._document.attachments.append(attachment_path)
        return self
    
    def set_custom_id(self, custom_id: str) -> 'ConcreteDocumentBuilder':
        """Permite establecer un ID personalizado"""
        self._document.document_id = custom_id
        return self
    
    def bulk_add_content(self, content_dict: Dict[str, Any]) -> 'ConcreteDocumentBuilder':
        """Añade múltiple contenido de una vez"""
        self._document.content.update(content_dict)
        return self
    
    def bulk_set_metadata(self, metadata_dict: Dict[str, Any]) -> 'ConcreteDocumentBuilder':
        """Añade múltiples metadatos de una vez"""
        self._document.metadata.update(metadata_dict)
        return self


class DocumentDirector:
    """
    Director que conoce cómo construir tipos específicos de documentos
    """
    
    def __init__(self, builder: DocumentBuilder):
        self._builder = builder
    
    @property
    def builder(self) -> DocumentBuilder:
        return self._builder
    
    @builder.setter
    def builder(self, builder: DocumentBuilder) -> None:
        self._builder = builder
    
    def build_ticket(self, movie_name: str, showtime: str, seat: str, 
                    client_name: str, image_path: Optional[str] = None,
                    ticket_price: float = 0.0) -> Document:
        """
        Construye un boleto de cine usando el patrón Builder
        """
        return (self._builder
                .set_document_type("cinema_ticket")
                .set_title("🎬 CINEMASTER - Boleto de Entrada")
                .set_subtitle(f"Película: {movie_name}")
                .add_content("movie_name", movie_name)
                .add_content("showtime", showtime)
                .add_content("seat", seat)
                .add_content("client_name", client_name)
                .add_content("ticket_price", ticket_price)
                .set_metadata("generated_by", "CineMaster API")
                .set_metadata("document_version", "1.0")
                .set_metadata("image_path", image_path)
                .set_styling("theme", "cinema")
                .set_styling("color_scheme", "dark_blue")
                .set_header("🎭 CINEMASTER CINEMA")
                .set_footer("¡Gracias por elegirnos! - www.cinemaster.com")
                .document)
    
    def build_invoice(self, client_name: str, items: List[Dict], 
                     total_amount: float) -> Document:
        """
        Construye una factura usando el patrón Builder
        """
        return (self._builder
                .set_document_type("invoice")
                .set_title("🧾 FACTURA - CINEMASTER")
                .set_subtitle(f"Cliente: {client_name}")
                .add_content("client_name", client_name)
                .add_content("items", items)
                .add_content("total_amount", total_amount)
                .set_metadata("generated_by", "CineMaster API")
                .set_metadata("document_version", "1.0")
                .set_styling("theme", "professional")
                .set_styling("color_scheme", "blue_white")
                .set_header("CINEMASTER - FACTURACIÓN")
                .set_footer("Documento generado automáticamente")
                .document)
    
    def build_report(self, report_title: str, report_data: Dict[str, Any],
                    report_type: str = "general") -> Document:
        """
        Construye un reporte usando el patrón Builder
        """
        return (self._builder
                .set_document_type("report")
                .set_title(f"📊 REPORTE - {report_title.upper()}")
                .set_subtitle(f"Tipo: {report_type}")
                .bulk_add_content(report_data)
                .set_metadata("generated_by", "CineMaster API")
                .set_metadata("report_type", report_type)
                .set_styling("theme", "analytical")
                .set_styling("color_scheme", "green_white")
                .set_header("CINEMASTER - REPORTES")
                .set_footer("Reporte generado automáticamente")
                .document)


# Instancia global del sistema Builder
_global_builder = ConcreteDocumentBuilder()
_global_director = DocumentDirector(_global_builder)


def get_document_builder() -> ConcreteDocumentBuilder:
    """
    Función global para obtener una nueva instancia del builder
    """
    return ConcreteDocumentBuilder()


def get_document_director(builder: Optional[DocumentBuilder] = None) -> DocumentDirector:
    """
    Función global para obtener el director con un builder específico o el global
    """
    if builder:
        return DocumentDirector(builder)
    return _global_director


# Funciones de conveniencia para uso rápido
def quick_build_ticket(movie_name: str, showtime: str, seat: str, 
                      client_name: str, image_path: Optional[str] = None,
                      ticket_price: float = 0.0) -> Document:
    """Función de conveniencia para crear boletos rápidamente"""
    director = get_document_director()
    return director.build_ticket(movie_name, showtime, seat, client_name, 
                               image_path, ticket_price)


def quick_build_invoice(client_name: str, items: List[Dict], 
                       total_amount: float) -> Document:
    """Función de conveniencia para crear facturas rápidamente"""
    director = get_document_director()
    return director.build_invoice(client_name, items, total_amount)


def quick_build_report(report_title: str, report_data: Dict[str, Any],
                      report_type: str = "general") -> Document:
    """Función de conveniencia para crear reportes rápidamente"""
    director = get_document_director()
    return director.build_report(report_title, report_data, report_type)
