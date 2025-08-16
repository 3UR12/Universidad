import requests
import json
import os

CACHE_PATH = "cache.json"
_cache = {}

# Cargar caché al inicio
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        try:
            _cache = json.load(f)
        except json.JSONDecodeError:
            _cache = {}

def get_json(url: str) -> dict:
    if url in _cache:
        return _cache[url]

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        # Validación mínima antes de guardar
        if isinstance(data, dict) and "name" in data:
            _cache[url] = data

        return data
    except (requests.RequestException, ValueError):
        return {}

def guardar_cache():
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(_cache, f, indent=None)
