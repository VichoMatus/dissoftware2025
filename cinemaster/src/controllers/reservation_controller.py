from models.seat_proxy import SeatProxy
from models.seat import Seat
from commands.reserve_seat_command import ReserveSeatCommand

class ReservationController:
    """
    Controlador responsable de la lógica de reserva de asientos.
    SRP: Solo maneja la lógica de reserva, no la UI.
    """
    def __init__(self, reservation_system=None):
        self.reservation_system = reservation_system

    def reservar_asiento(self, client_id, id_funcion, seat_id):
        seat = self.reservation_system.get_seat_by_id(seat_id)
        proxy = SeatProxy(seat)
        if not proxy.book_seat():
            raise ValueError("No se pudo reservar el asiento vía Proxy")
        command = ReserveSeatCommand(client_id, id_funcion, seat_id)
        reserva = command.execute()
        return reserva