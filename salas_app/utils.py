import re # Se importa la librería re para trabajar con expresiones regulares

def validar_rut(rut: str) -> bool:
    """
    Se válida el RUT chileno utilizando el algoritmo de módulo 11.
    Se aceptan formatos con o sin puntos y guion. El dígito verificador puede ser un número o 'k'. Ej: 12.345.678-5 o 12345678k.
    """
    if not rut:
        return False

    rut = rut.replace(".", "").replace("-", "").strip().lower()

    # Debe ser: 7 u 8 dígitos + dígito verificador (0-9 o k)
    if not re.match(r'^\d{7,8}[0-9k]$', rut):
        return False

    cuerpo = rut[:-1]
    dv = rut[-1]

    reversed_digits = list(map(int, reversed(cuerpo)))
    factores = [2, 3, 4, 5, 6, 7]
    suma = 0
    i = 0

    for digito in reversed_digits:
        suma += digito * factores[i]
        i = (i + 1) % len(factores)

    resto = suma % 11
    resultado = 11 - resto

    if resultado == 11:
        dv_calculado = '0'
    elif resultado == 10:
        dv_calculado = 'k'
    else:
        dv_calculado = str(resultado)

    return dv == dv_calculado
