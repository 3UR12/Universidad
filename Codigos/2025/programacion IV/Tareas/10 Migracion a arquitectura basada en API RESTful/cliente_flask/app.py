from flask import Flask
from vistas.libros import libros_bp
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_secreta_wey")
app.register_blueprint(libros_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
