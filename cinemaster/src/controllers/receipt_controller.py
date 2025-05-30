from commands.generate_receipt_command import GenerateReceiptCommand
from commands.invoker import Invoker

class ReceiptController:
    def __init__(self):
        self.invoker = Invoker()

    def generar_boleta(self, movie_name, showtime, seat, imagen, client_name="Cliente"):
        command = GenerateReceiptCommand(movie_name, showtime, seat, imagen, client_name)
        self.invoker.add_command(command)

    def confirmar_boleta(self):
        self.invoker.execute_commands()
        print("Boleta generada")