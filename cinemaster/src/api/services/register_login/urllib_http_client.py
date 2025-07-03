import urllib.request
import urllib.parse
import json
from typing import Dict, Any
from .http_client_interface import HttpClientInterface

class UrllibHttpClient(HttpClientInterface):
    """
    Implementación concreta de cliente HTTP usando urllib.
    Principio SRP (Single Responsibility) - Solo maneja peticiones HTTP
    Principio DIP (Dependency Inversion) - Implementa la abstracción
    """
    
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
    
    def make_request(self, endpoint: str, data: Dict[str, Any], method: str = "POST") -> Dict[str, Any]:
        """
        Realiza una petición HTTP usando urllib
        
        Args:
            endpoint: Endpoint de la API
            data: Datos a enviar
            method: Método HTTP
            
        Returns:
            Dict con la respuesta o error
        """
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                # Para GET, agregar parámetros a la URL
                if data:
                    query_string = urllib.parse.urlencode(data)
                    url = f"{url}?{query_string}"
                req = urllib.request.Request(url, method=method)
            else:
                # Para POST/PUT/etc, enviar datos en el body
                json_data = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(
                    url,
                    data=json_data,
                    headers={
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    method=method
                )
            
            # Realizar la petición
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)
                
        except urllib.error.HTTPError as e:
            return self._handle_http_error(e)
        except urllib.error.URLError as e:
            return {
                "success": False,
                "error": f"Error de conexión: {str(e)}. ¿Está la API funcionando?",
                "error_type": "connection_error"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error inesperado: {str(e)}",
                "error_type": "unexpected_error"
            }
    
    def _handle_http_error(self, error: urllib.error.HTTPError) -> Dict[str, Any]:
        """
        Maneja errores HTTP de manera consistente
        Principio SRP - Responsabilidad específica para manejo de errores
        """
        try:
            error_data = error.read().decode('utf-8')
            error_json = json.loads(error_data)
            return {
                "success": False,
                "error": error_json.get("detail", "Error desconocido"),
                "status_code": error.code,
                "error_type": "http_error"
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": f"Error HTTP {error.code}: {error_data if 'error_data' in locals() else 'Error desconocido'}",
                "status_code": error.code,
                "error_type": "http_error"
            }
