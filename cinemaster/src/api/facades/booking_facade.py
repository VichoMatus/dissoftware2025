from sqlalchemy.orm import Session
from typing import Dict, Any
from sqlalchemy import text

from api.commands import CommandInvoker, ReserveSeatCommand, GenerateReceiptCommand, NotificationCommand
from api.observers import ReservationSubject, EmailObserver

class BookingFacade:
    """
    Facade simple para el sistema de reservas de la API.
    Solo encapsula la lógica que ya existe en reservas.py
    """
    
    def __init__(self):
        # Componentes que ya tienes
        self.invoker = CommandInvoker()
        self.reservation_subject = ReservationSubject()
        self.email_observer = EmailObserver()
        
        # Configurar observer
        self.reservation_subject.attach(self.email_observer)
        
        print("🏢 BookingFacade inicializado")
    
    def book_complete_reservation(self, reservation_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Proceso completo de reserva - exactamente lo mismo que está en reservas.py
        """
        try:
            # 1. Verificar disponibilidad (igual que en reservas.py)
            if not self._check_seat_availability(reservation_data, db):
                return {
                    "success": False,
                    "error": "El asiento no está disponible para este horario o ya fue reservado."
                }
            
            # 2. Comando de reserva (igual que en reservas.py)
            reserve_command = ReserveSeatCommand(
                client_id=reservation_data["client_id"],
                id_funcion=reservation_data["id_funcion"],
                seat_id=reservation_data["seat_id"],
                db=db
            )
            
            reserva_resultado = self.invoker.execute_single_command(reserve_command)
            
            if not reserva_resultado.get("success"):
                return {
                    "success": False,
                    "error": reserva_resultado.get("error", "Error desconocido")
                }
            
            # 3. Comando de boleta (igual que en reservas.py)
            receipt_command = GenerateReceiptCommand(
                movie_name=reservation_data["movie_name"],
                showtime=reservation_data["showtime_string"],
                seat=reservation_data["seat_id"],
                client_name=reservation_data["cliente_nombre"],
                imagen=reservation_data.get("imagen"),
                ticket_price=reservation_data.get("costo_entrada", 12.0)
            )
            
            boleta_resultado = self.invoker.execute_single_command(receipt_command)
            
            # 4. Comando de notificación (igual que en reservas.py)
            notification_resultado = {"success": False}
            if reservation_data.get("cliente_email"):
                event_data = {
                    "cliente_email": reservation_data["cliente_email"],
                    "cliente_nombre": reservation_data["cliente_nombre"],
                    "movie_name": reservation_data["movie_name"],
                    "seat_id": reservation_data["seat_id"],
                    "showtime_string": reservation_data["showtime_string"],
                    "pdf_path": boleta_resultado.get("pdf_path"),
                    "reserva_id": reserva_resultado.get("reserva_seat_id"),
                    "reservation_id": reserva_resultado.get("reservation_id")
                }
                
                notification_command = NotificationCommand(
                    reservation_subject=self.reservation_subject,
                    event_data=event_data
                )
                
                notification_resultado = self.invoker.execute_single_command(notification_command)
            
            # Resultado final
            return {
                "success": True,
                "message": "Reserva confirmada exitosamente. Boleta generada y email enviado.",
                "reserva_id": reserva_resultado.get("reserva_seat_id"),
                "boleta_generada": boleta_resultado.get("success", False),
                "email_enviado": notification_resultado.get("success", False)
            }
            
        except Exception as e:
            print(f"❌ Error en BookingFacade: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _check_seat_availability(self, reservation_data: Dict[str, Any], db: Session) -> bool:
        """Misma verificación que está en reservas.py"""
        try:
            query = text("""
                SELECT ha.asiento_id 
                FROM horario_asientos ha 
                WHERE ha.asiento_id = :seat_id 
                  AND ha.horario_id = :id_funcion 
                  AND ha.Available = 1
            """)
            
            result = db.execute(query, {
                "seat_id": reservation_data["seat_id"],
                "id_funcion": reservation_data["id_funcion"]
            })
            
            return result.fetchone() is not None
            
        except Exception as e:
            print(f"❌ Error verificando disponibilidad: {e}")
            return False

# Instancia global
booking_facade = BookingFacade()