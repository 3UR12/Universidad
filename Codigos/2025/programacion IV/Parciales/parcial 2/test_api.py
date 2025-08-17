import pytest # Importa pytest para las pruebas
from app import app

# Cliente de prueba para la API
@pytest.fixture
def cliente():
    app.config["TESTING"] = True
    with app.test_client() as cliente:
        yield cliente

# Prueba: obtener todos los datos
def test_get_todos(cliente):
    respuesta = cliente.get("/vacunas")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.get_json(), list)

# Prueba: obtener año específico
def test_get_por_year(cliente):
    respuesta = cliente.get("/vacunas/2001")
    assert respuesta.status_code == 200
    assert respuesta.get_json()["year"] == 2001

# Prueba: año no existente
def test_get_año_invalido(cliente):
    respuesta = cliente.get("/vacunas/1990")
    assert respuesta.status_code == 404

# Prueba: simulación por provincia válida
def test_get_provincia_valida(cliente):
    respuesta = cliente.get("/vacunas/provincia/Panamá")
    assert respuesta.status_code == 200
    assert all(d["provincia"] == "Panamá" for d in respuesta.get_json())

# Prueba: provincia inválida
def test_get_provincia_invalida(cliente):
    respuesta = cliente.get("/vacunas/provincia/Narnia")
    assert respuesta.status_code == 404
