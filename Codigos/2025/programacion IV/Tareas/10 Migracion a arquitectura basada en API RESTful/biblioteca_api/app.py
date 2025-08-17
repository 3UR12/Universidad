#biblioteca_api/ app.py
from flask import Flask
from rutas_libros import libros_bp

app = Flask(__name__)
app.register_blueprint(libros_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
