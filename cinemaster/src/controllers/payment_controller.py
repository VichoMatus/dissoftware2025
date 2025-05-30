from commands.process_payment_command import ProcessPaymentCommand
from commands.invoker import Invoker

class PaymentController:
    def __init__(self, payment_system):
        self.payment_system = payment_system
        self.invoker = Invoker()

    def procesar_pago(self, payment_details):
        process_payment_command = ProcessPaymentCommand(payment_details, self.payment_system)
        self.invoker.add_command(process_payment_command)

    def confirmar_pago(self):
        self.invoker.execute_commands()
        print("Pago confirmado")
