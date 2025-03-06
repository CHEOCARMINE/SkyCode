import os
from flask_mail import Mail, Message

mail = Mail()

def init_mail(app):
    """Inicializa Flask-Mail en la aplicación."""
    mail.init_app(app)

def send_email(subject, recipients, body, html=None):
    """
    Envía un correo electrónico.

    :param subject: Asunto del correo.
    :param recipients: Lista de correos destino.
    :param body: Mensaje en texto plano.
    :param html: (Opcional) Mensaje en HTML.
    """
    msg = Message(subject, recipients=recipients, body=body, html=html)
    mail.send(msg)
