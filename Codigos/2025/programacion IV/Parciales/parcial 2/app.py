from flask import Flask
from routes import rutas

# Crea la aplicación Flask
app = Flask(__name__)

# Registra las rutas
app.register_blueprint(rutas)

# Ejecuta la API
if __name__ == "__main__":
    app.run(debug=True)
