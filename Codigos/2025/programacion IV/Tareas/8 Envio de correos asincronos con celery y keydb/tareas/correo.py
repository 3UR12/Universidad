from flask_mail import Mail, Message
from flask import Flask
from celery_app import celery
import os

app = Flask(__name__)
app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_USE_TLS=os.getenv("MAIL_USE_TLS") == "True",
    MAIL_USE_SSL=False
)

mail = Mail(app)

@celery.task
def enviar_correo(destinatario, asunto, cuerpo):
    with app.app_context():
        try:
            mensaje = Message(asunto, recipients=[destinatario], body=cuerpo)
            mail.send(mensaje)
        except Exception as e:
            print(f"Error al enviar correo: {e}")
