from abc import ABC, abstractmethod
from typing import Dict, Any

class AuthServiceInterface(ABC):
    """
    Interface para servicios de autenticación.
    Principio ISP (Interface Segregation) - Interface específica para autenticación
    """
    
    @abstractmethod
    def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        """Autentica un usuario"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Verifica la conexión del servicio"""
        pass

class RegistrationServiceInterface(ABC):
    """
    Interface para servicios de registro.
    Principio ISP (Interface Segregation) - Interface específica para registro
    """
    
    @abstractmethod
    def register_cliente(self, name: str, email: str, password: str, membership: bool = False) -> Dict[str, Any]:
        """Registra un nuevo cliente"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Verifica la conexión del servicio"""
        pass
