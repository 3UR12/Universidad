import uuid

def generar_id_unico():
    """
    Genera un identificador único para cada libro.
    """
    return str(uuid.uuid4())
