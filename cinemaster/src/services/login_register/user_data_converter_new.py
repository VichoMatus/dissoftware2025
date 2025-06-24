from typing import Dict, Any
from .auth_interfaces import IUserDataConverter

class UserDataConverter(IUserDataConverter):
    """
    Convertidor de datos de usuario de API a formato de aplicación
    Principio Single Responsibility: Solo se encarga de conversión de datos
    """
    
    def convert_user_data(self, user_data: Dict[str, Any], user_type: str) -> Any:
        """
        Convierte los datos del usuario de la API al formato esperado por la aplicación
        """
        if not user_data:
            return None
        
        # Factory Pattern para crear el tipo correcto de usuario
        converter_methods = {
            "cliente": self._create_cliente_data,
            "empleado": self._create_empleado_data,
            "admin": self._create_admin_data
        }
        
        converter = converter_methods.get(user_type)
        if converter:
            return converter(user_data)
        
        return None
    
    def _create_cliente_data(self, data: Dict[str, Any]) -> Any:
        """Crea objeto de datos de cliente"""
        class ClienteData:
            def __init__(self, user_data):
                self.cliente_id = user_data.get("id")
                self.nombre = user_data.get("nombre")
                self.Email = user_data.get("email")
                self.Membership = user_data.get("membership", False)
        
        return ClienteData(data)
    
    def _create_empleado_data(self, data: Dict[str, Any]) -> Any:
        """Crea objeto de datos de empleado"""
        class EmpleadoData:
            def __init__(self, user_data):
                self.employee_id = user_data.get("id")
                self.Name = user_data.get("name")
                self.Email = user_data.get("email")
        
        return EmpleadoData(data)
    
    def _create_admin_data(self, data: Dict[str, Any]) -> Any:
        """Crea objeto de datos de administrador"""
        class AdminData:
            def __init__(self, user_data):
                self.Admin_id = user_data.get("id")
                self.nombre = user_data.get("nombre")
                self.Email = user_data.get("email")
        
        return AdminData(data)
