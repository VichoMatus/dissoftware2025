from .seat import Seat
import tkinter.messagebox as messagebox

class SeatProxy:
    def __init__(self, seat: Seat):
        self._seat = seat
        self._locked = False

    def book_seat(self):
        print(f"[Proxy] Reservando asiento {self._seat.seat_id}...")
        messagebox.showinfo("Proxy", f"Reservando asiento {self._seat.seat_id}...")
        self._locked = True
        self._seat.book_seat()
        self._locked = False
        print(f"[Proxy] Asiento {self._seat.seat_id} reservado exitosamente")
        messagebox.showinfo("Proxy", f"Asiento {self._seat.seat_id} reservado exitosamente.")
        return True


    def update_seat_status(self):
        self._seat.update_seat_status()

    def get_status(self):
        return self._seat.status

    @property
    def seat_id(self):
        return self._seat.seat_id

    @property
    def row(self):
        return self._seat.row

    @property
    def column(self):
        return self._seat.column
