import os

def combinar_archivos(directorio, archivo_salida):
    contenido_total = ""
    
    # Recorrer todos los archivos en el directorio
    for raiz, dirs, archivos in os.walk(directorio):
        # Omitir directorios __pycache__
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        
        for archivo in archivos:
            ruta_archivo = os.path.join(raiz, archivo)
            
            # Leer el contenido de cada archivo
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    contenido_total += f"\n\n--- Contenido de {ruta_archivo} ---\n\n"
                    contenido_total += contenido
            except Exception as e:
                print(f"Error al leer {ruta_archivo}: {str(e)}")
    
    # Escribir todo el contenido en el archivo de salida
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(contenido_total)

# Directorio del proyecto y archivo de salida
directorio_app = "app/"
archivo_salida = "contenido_combinado.txt"

# Ejecutar la función
combinar_archivos(directorio_app, archivo_salida)

print(f"Se ha creado el archivo {archivo_salida} con el contenido de todos los archivos en {directorio_app}, excluyendo las carpetas __pycache__")