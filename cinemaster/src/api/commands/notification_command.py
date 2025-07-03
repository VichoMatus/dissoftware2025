from .command import Command
from api.observers import ReservationSubject
from typing import Dict, Any

class NotificationCommand(Command):
    """
    Comando para manejar notificaciones usando el patrón Observer.
    Se encarga de notificar a todos los observadores registrados cuando se confirma una reserva.
    """
    
    def __init__(self, reservation_subject: ReservationSubject, event_data: Dict[str, Any]):
        self.reservation_subject = reservation_subject
        self.event_data = event_data
    
    def execute(self) -> Dict[str, Any]:
        """
        Ejecuta la notificación a todos los observadores.
        
        Returns:
            Dict con el resultado de las notificaciones enviadas
        """
        try:
            print(f"🔔 Ejecutando NotificationCommand para {self.event_data.get('cliente_nombre')}")
            
            # Notificar a todos los observadores a través del subject
            self.reservation_subject.reservation_confirmed(self.event_data)
            
            # Obtener información sobre cuántos observadores fueron notificados
            num_observers = len(self.reservation_subject._observers)
            
            return {
                "success": True,
                "message": f"Notificaciones enviadas a {num_observers} observador(es)",
                "observers_notified": num_observers,
                "cliente_notificado": self.event_data.get("cliente_nombre"),
                "email_enviado_a": self.event_data.get("cliente_email")
            }
            
        except Exception as e:
            print(f"❌ Error en NotificationCommand: {e}")
            return {
                "success": False,
                "message": f"Error enviando notificaciones: {str(e)}",
                "observers_notified": 0,
                "error": str(e)
            }