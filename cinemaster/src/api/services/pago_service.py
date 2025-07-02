from pydantic import BaseModel

class PagoRequest(BaseModel):
    client_id: int
    id_funcion: int
    seat_id: str
    movie_name: str
    showtime_string: str
    imagen: str
    cliente_nombre: str
    costo_entrada: float
    metodo_pago: str
    cliente_email: str  # <-- AGREGA ESTO SI QUIERES PASAR EL EMAIL


def procesar_pago(pago: PagoRequest):
    # Aquí va la lógica real de pago y reserva
    # Por ejemplo: reservar asiento, guardar en DB, enviar email, etc.
    # Simulación de respuesta:
    return {
        "status": "ok",
        "reservation_id": 123,
        "msg": f"Pago y reserva exitosos para {pago.movie_name} ({pago.seat_id})"
    }