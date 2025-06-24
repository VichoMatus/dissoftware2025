from abc import ABC, abstractmethod
from typing import Dict, Any

class IAuthService(ABC):
    """
    Interface para servicios de autenticación
    Principio Interface Segregation: Interface específica para autenticación
    """
    
    @abstractmethod
    def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        """
        Autentica un usuario con email y contraseña
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            
        Returns:
            Dict con resultado de autenticación:
            {
                "success": bool,
                "tipo_usuario": str,  # "cliente", "empleado", "admin"
                "usuario": object,    # datos del usuario
                "error": str          # mensaje de error si success=False
            }
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Prueba la conexión del servicio
        
        Returns:
            bool: True si la conexión es exitosa
        """
        pass


class IRegistrationService(ABC):
    """
    Interface para servicios de registro
    Principio Interface Segregation: Interface específica para registro
    """
    
    @abstractmethod
    def register_cliente(self, name: str, email: str, password: str, membership: bool = False) -> Dict[str, Any]:
        """
        Registra un nuevo cliente
        
        Args:
            name: Nombre del cliente
            email: Email del cliente
            password: Contraseña del cliente
            membership: Si tiene membresía (por defecto False)
            
        Returns:
            Dict con resultado del registro:
            {
                "success": bool,
                "cliente": object,    # objeto cliente si success=True
                "error": str          # mensaje de error si success=False
            }
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Prueba la conexión del servicio
        
        Returns:
            bool: True si la conexión es exitosa
        """
        pass


class IUserDataConverter(ABC):
    """
    Interface para convertidores de datos de usuario
    Principio Single Responsibility: Solo se encarga de convertir datos
    """
    
    @abstractmethod
    def convert_user_data(self, user_data: Dict[str, Any], user_type: str) -> Any:
        """
        Convierte datos de usuario de API a formato de aplicación
        
        Args:
            user_data: Datos del usuario desde la API
            user_type: Tipo de usuario ("cliente", "empleado", "admin")
            
        Returns:
            Objeto convertido según el tipo de usuario
        """
        pass
