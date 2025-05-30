from .command import Command

class ProcessPaymentCommand(Command):
    def __init__(self, payment_details, payment_system):
        self.payment_details = payment_details
        self.payment_system = payment_system

    def execute(self):
        # Lógica para procesar el pago
        self.payment_system.process_payment(self.payment_details)
