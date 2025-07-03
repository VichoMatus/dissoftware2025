import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Dict, Any

from .observer import Observer

# Importar configuración desde config.py
try:
    from config import EMAIL_SENDER, EMAIL_PASSWORD
    print(f"✅ Configuración de email cargada: {EMAIL_SENDER}")
except ImportError:
    print("⚠️ No se pudo cargar config.py - usando valores por defecto")
    EMAIL_SENDER = "cinemaster2006@gmail.com"
    EMAIL_PASSWORD = "skbm rhbh qbke rqir"

class EmailObserver(Observer):
    """
    Observador que envía emails cuando se confirma una reserva.
    Usa la configuración real desde config.py
    """
    
    def __init__(self):
        # Usar configuración desde config.py
        self.sender_email = EMAIL_SENDER
        self.sender_password = EMAIL_PASSWORD
        # Configuración SMTP para Gmail
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        print(f"📧 EmailObserver configurado con: {self.sender_email}")
    
    def update(self, event_data: Dict[str, Any]):
        """
        Recibe notificación de reserva confirmada y envía email.
        """
        try:
            cliente_email = event_data.get("cliente_email")
            cliente_nombre = event_data.get("cliente_nombre")
            movie_name = event_data.get("movie_name")
            
            if not cliente_email or not cliente_nombre:
                print("⚠️ Datos insuficientes para enviar email")
                return
            
            print(f"📤 Enviando email de {self.sender_email} a {cliente_email}")
            
            self.send_confirmation_email(
                to_email=cliente_email,
                client_name=cliente_nombre,
                movie_name=movie_name,
                seat_id=event_data.get("seat_id"),
                showtime=event_data.get("showtime_string"),
                pdf_path=event_data.get("pdf_path")
            )
            
        except Exception as e:
            print(f"❌ Error en EmailObserver: {e}")
    
    def send_confirmation_email(self, to_email: str, client_name: str, movie_name: str, 
                               seat_id: str = None, showtime: str = None, pdf_path: str = None):
        """
        Envía email de confirmación con boleta adjunta usando la configuración real.
        """
        try:
            print(f"🔄 Preparando email para {to_email}...")
            
            # Crear mensaje
            subject = f"🎬 Confirmación de Reserva - {movie_name}"
            
            body = f"""
¡Hola {client_name}!

¡Tu reserva ha sido confirmada exitosamente! 🎉

📋 DETALLES DE TU RESERVA:
🎬 Película: {movie_name}
📅 Horario: {showtime if showtime else 'Por confirmar'}
💺 Asiento: {seat_id if seat_id else 'Por asignar'}

📧 Si tienes alguna pregunta, no dudes en contactarnos:
📞 Teléfono: +56 9 6969 6969
📧 Email: {self.sender_email}

¡Gracias por elegir CineMaster! 🍿

---
Este es un email automático generado por el sistema CineMaster.
            """
            
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Adjuntar PDF si existe
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
                    pdf_filename = os.path.basename(pdf_path)
                    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
                    msg.attach(pdf_attachment)
                print(f"📎 PDF adjuntado: {pdf_filename}")
            else:
                print("⚠️ No se encontró PDF para adjuntar")
            
            # Conectar y enviar email
            print(f"🔌 Conectando a {self.smtp_server}:{self.smtp_port}...")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                print("🔐 Iniciando conexión segura...")
                server.starttls()
                
                print(f"🔑 Autenticando con {self.sender_email}...")
                server.login(self.sender_email, self.sender_password)
                
                print(f"📤 Enviando email a {to_email}...")
                server.sendmail(self.sender_email, to_email, msg.as_string())
            
            print(f"✅ Email enviado exitosamente a {to_email}")
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Error de autenticación SMTP: {e}")
            print(f"   Email: {self.sender_email}")
            print(f"   Password usado: {self.sender_password[:4]}****")
            print("   Verifica que la contraseña de aplicación sea correcta")
        except smtplib.SMTPRecipientsRefused as e:
            print(f"❌ Email rechazado: {e}")
            print(f"   Verifica que {to_email} sea un email válido")
        except smtplib.SMTPException as e:
            print(f"❌ Error SMTP: {e}")
        except Exception as e:
            print(f"❌ Error enviando email: {e}")