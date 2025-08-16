from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

celery = Celery(
    "correo",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend="redis://localhost:6379/1"
)
