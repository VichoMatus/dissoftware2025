from commands.reserve_seat_command import ReserveSeatCommand

class ReservationController:
    def __init__(self, reservation_system=None):
        # Aquí puedes decidir si necesitas usar 'reservation_system' o no
        self.reservation_system = reservation_system  # Solo lo usa si lo necesitas
        # No hace falta 'reservation_system' si no lo usas en este controlador

    def reservar_asiento(self, client_id, id_funcion, seat_id):
        command = ReserveSeatCommand(client_id, id_funcion, seat_id)
        reserva = command.execute()
        return reserva
