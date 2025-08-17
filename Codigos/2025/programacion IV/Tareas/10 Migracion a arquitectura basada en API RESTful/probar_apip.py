import requests

API_URL = "http://localhost:5001/books"
data = {"titulo": "Test", "autor": "Copilot"}

try:
    r = requests.post(API_URL, json=data)
    print("Status:", r.status_code)
    print("Respuesta:", r.json())
except Exception as e:
    print("Error:", e)
