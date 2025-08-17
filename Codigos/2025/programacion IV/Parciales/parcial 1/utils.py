# Verifica que un valor no esté vacío
def validar_no_vacio(valor):
    return valor.strip() != ""

# Verifica que un valor sea numérico entero
def validar_entero(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False

# Verifica que un valor sea numérico decimal
def validar_decimal(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False
