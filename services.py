from flask_mail import Mail, Message
from flask import current_app
import os

mail = Mail()

def init_mail(app):
    """Inicializa Flask-Mail en la aplicación."""
    mail.init_app(app)

def send_email(subject, recipients, body, html=None, attachments=None):
    """
    Envía un correo electrónico.

    :param subject: Asunto del correo.
    :param recipients: Lista de correos destino.
    :param body: Mensaje en texto plano.
    :param html: (Opcional) Mensaje en HTML.
    :param attachments: (Opcional) Lista de rutas de archivos a adjuntar.
    """
    msg = Message(subject, recipients=recipients, body=body, html=html)

    if attachments:
        for path in attachments:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    filename = os.path.basename(path)
                    msg.attach(filename, "application/pdf", f.read())

    mail.send(msg)
