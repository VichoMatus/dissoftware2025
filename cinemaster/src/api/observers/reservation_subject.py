from typing import Dict, Any
from .observer import Subject

class ReservationSubject(Subject):
    """
    Sujeto que notifica cuando se confirma una reserva.
    Mantiene lista de observadores y les notifica sobre eventos de reserva.
    """
    
    def __init__(self):
        super().__init__()
        self.last_reservation_data = None
    
    def reservation_confirmed(self, reservation_data: Dict[str, Any]):
        """
        Método llamado cuando se confirma una reserva.
        Notifica a todos los observadores registrados.
        
        Args:
            reservation_data: Datos de la reserva confirmada
        """
        try:
            self.last_reservation_data = reservation_data
            print(f"🔔 Notificando reserva confirmada para {reservation_data.get('cliente_nombre')}")
            
            # Notificar a todos los observadores
            self.notify(reservation_data)
            
        except Exception as e:
            print(f"❌ Error notificando reserva: {e}")
    
    def get_last_reservation(self) -> Dict[str, Any]:
        """Devuelve los datos de la última reserva procesada"""
        return self.last_reservation_data