from datetime import datetime

class ClienteService:
    @staticmethod
    def obtener_reservas_actuales(cliente):
        ahora = datetime.now()
        return [r for r in cliente.reservas if r.funcion and r.funcion.Schedule >= ahora]

    @staticmethod
    def obtener_historial_reservas(cliente):
        ahora = datetime.now()
        return [r for r in cliente.reservas if r.funcion and r.funcion.Schedule < ahora]

    @staticmethod
    def clonar_cliente(cliente):
        import copy
        cliente_clonado = copy.copy(cliente)
        cliente_clonado.cliente_id = None
        cliente_clonado.Reservation_history = ""
        return cliente_clonado