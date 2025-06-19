from typing import Dict, Any
from .interfaces import RegistrationServiceInterface
from .http_client_interface import HttpClientInterface
from .urllib_http_client import UrllibHttpClient
from .api_auth_service import UserDataFactory

class ApiRegistrationService(RegistrationServiceInterface):
    """
    Servicio de registro que usa la API.
    
    Principios SOLID aplicados:
    - SRP: Solo maneja registro de usuarios vía API
    - OCP: Extensible sin modificar código existente
    - LSP: Sustituible por cualquier implementación de RegistrationServiceInterface
    - ISP: Implementa solo la interface de registro
    - DIP: Depende de abstracciones, no de implementaciones concretas
    """
    
    def __init__(self, http_client: HttpClientInterface = None, api_base_url: str = "http://127.0.0.1:8000"):
        # DIP: Inyección de dependencias
        self._http_client = http_client or UrllibHttpClient(api_base_url)
        self._user_data_factory = UserDataFactory()
        self._validator = RegistrationValidator()
    
    def register_cliente(self, name: str, email: str, password: str, membership: bool = False) -> Dict[str, Any]:
        """
        Registra un nuevo cliente usando la API
        
        Args:
            name: Nombre del cliente
            email: Email del cliente
            password: Contraseña del cliente
            membership: Si tiene membresía
            
        Returns:
            Dict con resultado del registro
        """
        # Validar datos de entrada
        validation_result = self._validator.validate_registration_data(name, email, password)
        if not validation_result["valid"]:
            return {
                "success": False,
                "error": validation_result["error"]
            }
        
        # Preparar datos para la API
        registration_data = {
            "email": email.strip(),
            "password": password.strip()
        }
        
        # Realizar petición a la API
        response = self._http_client.make_request("/auth/register", registration_data)
        
        # Procesar respuesta
        return self._process_registration_response(response)
    
    def test_connection(self) -> bool:
        """
        Verifica la conexión con la API
        """
        try:
            response = self._http_client.make_request("/health", {}, "GET")
            return response.get("status") == "OK"
        except:
            return False
    
    def _process_registration_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa la respuesta de registro
        SRP: Responsabilidad específica de procesamiento de respuesta
        """
        if not response.get("success"):
            return {
                "success": False,
                "error": response.get("error", "Error en el registro")
            }
        
        cliente_data = response.get("cliente")
        if cliente_data:
            # Usar factory para crear objeto cliente
            cliente = self._user_data_factory.create_user(cliente_data, "cliente")
            return {
                "success": True,
                "cliente": cliente
            }
        
        return {
            "success": False,
            "error": "No se pudo crear el cliente"
        }

class RegistrationValidator:
    """
    Validador para datos de registro.
    Principio SRP: Solo se encarga de validar datos de registro
    Principio OCP: Fácil de extender con nuevas validaciones
    """
    
    def validate_registration_data(self, name: str, email: str, password: str) -> Dict[str, Any]:
        """
        Valida los datos de registro
        
        Returns:
            Dict con resultado de validación
        """
        # Validar email
        if not self._validate_email(email):
            return {
                "valid": False,
                "error": "El correo electrónico debe contener '@'"
            }
        
        # Validar contraseña
        if not self._validate_password(password):
            return {
                "valid": False,
                "error": "La contraseña debe tener al menos 4 caracteres"
            }
        
        # Validar nombre (opcional, ya que la API usa email como base)
        if name and not self._validate_name(name):
            return {
                "valid": False,
                "error": "El nombre no puede estar vacío"
            }
        
        return {"valid": True}
    
    def _validate_email(self, email: str) -> bool:
        """Valida formato de email"""
        if not email or not email.strip():
            return False
        return "@" in email.strip()
    
    def _validate_password(self, password: str) -> bool:
        """Valida contraseña"""
        if not password:
            return False
        return len(password.strip()) >= 4
    
    def _validate_name(self, name: str) -> bool:
        """Valida nombre"""
        if not name:
            return True  # Nombre es opcional
        return len(name.strip()) > 0
