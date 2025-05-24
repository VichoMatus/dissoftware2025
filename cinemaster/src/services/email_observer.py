import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from src.services.receipt_system import generate_receipt_text
from src.config import EMAIL_SENDER, EMAIL_PASSWORD

class EmailSenderObserver:
    def __init__(self):
        self.sender_email = EMAIL_SENDER
        self.sender_password = EMAIL_PASSWORD

    def update(self, reserva):
        cliente = reserva.client
        funcion = reserva.funcion
        pelicula = funcion.pelicula.Title if funcion and funcion.pelicula else "desconocida"

        receipt_text = generate_receipt_text(reserva.reservation_id)

        if not cliente or not cliente.Email:
            print("No se encontró el email del cliente.")
            return

        self.send_email(cliente.Email, cliente.nombre, pelicula, receipt_text)

    def send_email(self, to_email, client_name, movie_name, receipt_text):
        subject = "Su Boleta/Comprobante"
        body = f"Hola {client_name},\n\nGracias por su compra. Aquí está su boleta adjunta.\n\n{receipt_text}"

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        safe_client = client_name.strip().replace(" ", "_")
        safe_movie = movie_name.strip().replace(" ", "_")
        pdf_filename = f"boleta_{safe_client}_{safe_movie}.pdf"
        pdf_path = os.path.abspath(os.path.join("Boletas", pdf_filename))

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                part = MIMEApplication(f.read(), _subtype="pdf")
                part.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
                msg.attach(part)
        else:
            print(f"⚠️ No se encontró el PDF en: {pdf_path}")

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, msg.as_string())
            print(f"📤 Correo enviado a {to_email}")
        except Exception as e:
            print(f"❌ Error al enviar correo: {e}")
