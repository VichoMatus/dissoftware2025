from typing import Dict, Any
from .interfaces import AuthServiceInterface
from .http_client_interface import HttpClientInterface
from .urllib_http_client import UrllibHttpClient

class ApiAuthService(AuthServiceInterface):
    """
    Servicio de autenticación que usa la API.
    
    Principios SOLID aplicados:
    - SRP: Solo maneja autenticación vía API
    - OCP: Extensible sin modificar código existente
    - LSP: Sustituible por cualquier implementación de AuthServiceInterface
    - ISP: Implementa solo la interface de autenticación
    - DIP: Depende de abstracciones (HttpClientInterface), no de implementaciones concretas
    """
    
    def __init__(self, http_client: HttpClientInterface = None, api_base_url: str = "http://127.0.0.1:8000"):
        # DIP: Inyección de dependencias - depende de la abstracción, no de la implementación
        self._http_client = http_client or UrllibHttpClient(api_base_url)
        self._user_data_factory = UserDataFactory()
    
    def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        """
        Autentica un usuario usando la API
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            
        Returns:
            Dict con resultado de autenticación
        """
        # Validación básica
        if not self._validate_credentials(email, password):
            return {
                "success": False,
                "error": "Credenciales inválidas"
            }
        
        # Preparar datos para la API
        login_data = {
            "email": email.strip(),
            "password": password.strip()
        }
        
        # Realizar petición a la API
        response = self._http_client.make_request("/auth/login", login_data)
        
        # Procesar respuesta
        return self._process_auth_response(response)
    
    def test_connection(self) -> bool:
        """
        Verifica la conexión con la API
        """
        try:
            response = self._http_client.make_request("/health", {}, "GET")
            return response.get("status") == "OK"
        except:
            return False
    
    def _validate_credentials(self, email: str, password: str) -> bool:
        """
        Valida las credenciales básicas
        SRP: Responsabilidad específica de validación
        """
        if not email or not password:
            return False
        if "@" not in email:
            return False
        return True
    
    def _process_auth_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa la respuesta de autenticación
        SRP: Responsabilidad específica de procesamiento de respuesta
        """
        if not response.get("success"):
            return {
                "success": False,
                "error": response.get("error", "Error de autenticación")
            }
        
        user_type = response.get("user_type")
        user_data = response.get("user_data")
        
        # Usar factory para crear objeto usuario
        usuario = self._user_data_factory.create_user(user_data, user_type)
        
        return {
            "success": True,
            "tipo_usuario": user_type,
            "usuario": usuario
        }

class UserDataFactory:
    """
    Factory para crear objetos de usuario.
    Principio SRP: Solo se encarga de crear objetos usuario
    Principio OCP: Fácil de extender para nuevos tipos de usuario
    """
    
    def create_user(self, user_data: Dict[str, Any], user_type: str) -> Any:
        """
        Crea un objeto usuario según el tipo
        """
        if not user_data:
            return None
        
        creators = {
            "cliente": self._create_cliente,
            "empleado": self._create_empleado,
            "admin": self._create_admin
        }
        
        creator = creators.get(user_type)
        if creator:
            return creator(user_data)
        
        return None
    
    def _create_cliente(self, data: Dict[str, Any]) -> 'ClienteData':
        """Crea objeto ClienteData"""
        return ClienteData(data)
    
    def _create_empleado(self, data: Dict[str, Any]) -> 'EmpleadoData':
        """Crea objeto EmpleadoData"""
        return EmpleadoData(data)
    
    def _create_admin(self, data: Dict[str, Any]) -> 'AdminData':
        """Crea objeto AdminData"""
        return AdminData(data)

# Data Transfer Objects (DTOs)
class ClienteData:
    """
    DTO para datos de cliente
    SRP: Solo almacena datos de cliente
    """
    def __init__(self, data: Dict[str, Any]):
        self.cliente_id = data.get("id")
        self.nombre = data.get("nombre")
        self.Email = data.get("email")
        self.Membership = data.get("membership", False)

class EmpleadoData:
    """
    DTO para datos de empleado
    SRP: Solo almacena datos de empleado
    """
    def __init__(self, data: Dict[str, Any]):
        self.employee_id = data.get("id")
        self.Name = data.get("name")
        self.Email = data.get("email")

class AdminData:
    """
    DTO para datos de administrador
    SRP: Solo almacena datos de administrador
    """
    def __init__(self, data: Dict[str, Any]):
        self.Admin_id = data.get("id")
        self.nombre = data.get("nombre")
        self.Email = data.get("email")
