def limpiar_rut(rut: str) -> str:
    """
    Limpia el RUT de puntos y guiones, dejando solo números y la letra K si existe.
    """
    return rut.upper().replace(".", "").replace("-", "")

def calcular_digito_verificador(rut_numero: str) -> str:
    """
    Calcula el dígito verificador de un RUT.
    """
    try:
        serie = [2, 3, 4, 5, 6, 7]
        suma = 0
        
        for i, num in enumerate(reversed(rut_numero)):
            suma += int(num) * serie[i % len(serie)]
        
        resto = suma % 11
        if resto == 0:
            return '0'
        elif resto == 1:
            return 'K'
        else:
            return str(11 - resto)
    except:
        return ''

def validar_rut(rut: str) -> bool:
    """
    Valida un RUT chileno.
    Retorna True si el RUT es válido, False en caso contrario.
    """
    try:
        rut_limpio = limpiar_rut(rut)
        
        # Verificar longitud mínima y máxima
        if len(rut_limpio) < 2 or len(rut_limpio) > 9:
            return False
        
        # Separar número y dígito verificador
        rut_numero = rut_limpio[:-1]
        digito_verificador = rut_limpio[-1]
        
        # Verificar que el número del RUT sea válido
        if not rut_numero.isdigit():
            return False
        
        # Verificar que el dígito verificador sea válido (número o 'K')
        if not (digito_verificador.isdigit() or digito_verificador == 'K'):
            return False
        
        # Calcular y comparar el dígito verificador
        digito_calculado = calcular_digito_verificador(rut_numero)
        return digito_verificador == digito_calculado
        
    except:
        return False

def formatear_rut(rut: str) -> str:
    """
    Formatea un RUT a formato estándar (sin puntos, con guión)
    Ejemplo: 12345678-9
    """
    rut_limpio = limpiar_rut(rut)
    return f"{rut_limpio[:-1]}-{rut_limpio[-1]}"