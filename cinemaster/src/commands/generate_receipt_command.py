from .command import Command
from builders.receipt_builder import ReceiptBuilder
import os

class GenerateReceiptCommand(Command):
    def __init__(self, movie_name, showtime, seat, image, client_name="Cliente"):
        self.movie_name = movie_name
        self.showtime = showtime
        self.seat = seat
        self.image = image
        self.client_name = client_name

    def execute(self):
        builder = ReceiptBuilder()
        boleta = (
            builder
            .set_movie_name(self.movie_name)
            .set_showtime(self.showtime)
            .set_seat(self.seat)
            .set_image(self.image)
            .set_client_name(self.client_name)
            .build()
        )

        # Formato seguro del nombre
        safe_client = self.client_name.strip().replace(" ", "_")
        safe_movie = self.movie_name.strip().replace(" ", "_")
        filename = f"boleta_{safe_client}_{safe_movie}.pdf"

        # Asegurar que la carpeta exista
        output_dir = "Boletas"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, filename)
        boleta.generate_receipt(output_path)
