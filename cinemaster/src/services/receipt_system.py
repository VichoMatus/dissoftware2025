from database.db_connection import get_reservation_details

class ReceiptSystem:
    def generar_boleta(self, movie_name, showtime_string, seat, imagen, cliente_nombre):
        print("Boleta generada:")
        print(f"Película: {movie_name}")
        print(f"Hora: {showtime_string}")
        print(f"Asiento: {seat}")
        print(f"Cliente: {cliente_nombre}")
        print(f"Imagen: {imagen}")

    def confirmar_boleta(self):
        print("Boleta confirmada correctamente.")

def generate_receipt_text(reservation_id):
    details = get_reservation_details(reservation_id)

    if not details:
        return "No se pudo generar la boleta."

    receipt = (
        f"Película: {details['movie_name']}\n"
        f"Función: {details['showtime_string']}\n"
        f"Asiento: {details['seat']}\n"
        f"Cliente: {details['cliente_nombre']}\n"
        f"Precio: ${details['price']:.2f}\n"
        f"Gracias por su compra."
    )
    return receipt
