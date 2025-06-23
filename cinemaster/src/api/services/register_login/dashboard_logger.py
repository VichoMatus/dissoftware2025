from typing import Dict, Any
from datetime import datetime
from .http_client_interface import HttpClientInterface
from .urllib_http_client import UrllibHttpClient

class DashboardLogger:
    """
    Servicio para registrar acciones del cliente en el dashboard de la API.
    
    Principios SOLID aplicados:
    - SRP: Solo maneja el logging de acciones hacia la API
    - DIP: Depende de abstracciones (HttpClientInterface)
    - OCP: Extensible para nuevos tipos de acciones
    """
    
    def __init__(self, http_client: HttpClientInterface = None, api_base_url: str = "http://127.0.0.1:8000"):
        self._http_client = http_client or UrllibHttpClient(api_base_url)
        self._is_enabled = True
    
    def set_current_client(self, client_name: str, client_id: int, email: str) -> bool:
        """
        Establece el cliente actual en el dashboard
        
        Args:
            client_name: Nombre del cliente
            client_id: ID del cliente
            email: Email del cliente
            
        Returns:
            bool: True si se pudo establecer
        """
        if not self._is_enabled:
            return False
            
        try:
            client_data = {
                "client_name": client_name,
                "client_id": client_id,
                "email": email
            }
            
            response = self._http_client.make_request("/dashboard/client-login", client_data)
            return response.get("success", False)
        except:
            self._is_enabled = False  # Desactivar si hay error
            return False
    
    def log_action(self, action_type: str, description: str, details: Dict[str, Any] = None) -> bool:
        """
        Registra una acción del cliente
        
        Args:
            action_type: Tipo de acción (ej: MOVIE_SELECTED, SEAT_RESERVED)
            description: Descripción de la acción
            details: Detalles adicionales
            
        Returns:
            bool: True si se pudo registrar
        """
        if not self._is_enabled:
            return False
            
        try:
            action_data = {
                "action_type": action_type,
                "description": description,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "details": details or {}
            }
            
            response = self._http_client.make_request("/dashboard/log-action", action_data)
            return response.get("success", False)
        except:
            self._is_enabled = False  # Desactivar si hay error
            return False
    
    def log_movie_selection(self, movie_title: str, movie_id: int = None) -> bool:
        """
        Registra selección de película
        """
        return self.log_action(
            "MOVIE_SELECTED",
            f"Película seleccionada: {movie_title}",
            {"movie_title": movie_title, "movie_id": movie_id}
        )
    
    def log_seat_reservation(self, movie_title: str, seat_number: str, show_time: str = None) -> bool:
        """
        Registra reserva de asiento
        """
        return self.log_action(
            "SEAT_RESERVED",
            f"Asiento reservado: {seat_number} para {movie_title}",
            {"movie_title": movie_title, "seat_number": seat_number, "show_time": show_time}
        )
    
    def log_payment(self, amount: float, payment_method: str = None) -> bool:
        """
        Registra pago realizado
        """
        return self.log_action(
            "PAYMENT_COMPLETED",
            f"Pago realizado: ${amount}",
            {"amount": amount, "payment_method": payment_method}
        )
    
    def log_cartelera_view(self) -> bool:
        """
        Registra que el usuario está viendo la cartelera
        """
        return self.log_action(
            "CARTELERA_VIEWED",
            "Cliente está navegando por la cartelera"
        )
    
    def disable(self):
        """Desactiva el logger (útil si la API no está disponible)"""
        self._is_enabled = False
    
    def enable(self):
        """Reactiva el logger"""
        self._is_enabled = True
