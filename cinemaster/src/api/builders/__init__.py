"""
Módulo de patrones Builder para CineMaster API
Implementa el patrón Builder de forma global y reutilizable
"""

from .document_builder import (
    Document,
    DocumentBuilder,
    ConcreteDocumentBuilder,
    DocumentDirector,
    get_document_builder,
    get_document_director,
    quick_build_ticket,
    quick_build_invoice,
    quick_build_report
)

from .document_processor import (
    DocumentProcessor,
    get_document_processor
)

__all__ = [
    'Document',
    'DocumentBuilder', 
    'ConcreteDocumentBuilder',
    'DocumentDirector',
    'DocumentProcessor',
    'get_document_builder',
    'get_document_director',
    'get_document_processor',
    'quick_build_ticket',
    'quick_build_invoice',
    'quick_build_report'
]
