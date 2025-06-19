from abc import ABC, abstractmethod
from typing import Dict, Any

class HttpClientInterface(ABC):
    """
    Interface para clientes HTTP.
    Principio DIP (Dependency Inversion) - Abstracción para clientes HTTP
    """
    
    @abstractmethod
    def make_request(self, endpoint: str, data: Dict[str, Any], method: str = "POST") -> Dict[str, Any]:
        """Realiza una petición HTTP"""
        pass
