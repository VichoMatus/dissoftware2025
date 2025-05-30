from services.payment_system import PaymentSystem
from services.receipt_system import ReceiptSystem
from services.reservation_system import ReservationSystem

from controllers.reservation_controller import ReservationController
from controllers.payment_controller import PaymentController
from controllers.receipt_controller import ReceiptController

from models.database import HorarioAsientos, get_db

class BookingFacade:
    def __init__(self):
        self._observers = []

        self.reservation_system = ReservationSystem()
        self.payment_system = PaymentSystem()
        self.receipt_system = ReceiptSystem()

        self.reservation = ReservationController(self.reservation_system)
        self.payment = PaymentController(self.payment_system)
        self.receipt = ReceiptController()

    def register_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, reserva):
        for obs in self._observers:
            obs.update(reserva)

    def book_ticket(self, reservation_data, payment_data, receipt_data):
        reserva = self.reservation.reservar_asiento(
            reservation_data["client_id"],
            reservation_data["id_funcion"],
            reservation_data["seat_id"]
        )

        self.payment.procesar_pago(payment_data)
        self.payment.confirmar_pago()

        self.receipt.generar_boleta(
            receipt_data["movie_name"],
            receipt_data["showtime_string"],
            receipt_data["seat"],
            receipt_data["imagen"],
            receipt_data["cliente_nombre"]
        )

        self.receipt.confirmar_boleta()

        self.notify_observers(reserva)

        return reserva
    def get_available_seats(self, showtime_id):
        db = next(get_db())
        horario_asientos = db.query(HorarioAsientos)\
            .filter(HorarioAsientos.horario_id == showtime_id, HorarioAsientos.Available == True).all()
        
        available_seats = []
        for ha in horario_asientos:
            asiento = ha.asiento
            if asiento:
                available_seats.append(asiento.ids_seats)
        return available_seats