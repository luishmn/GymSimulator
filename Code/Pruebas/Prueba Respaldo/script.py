import os
import shutil

def restaurar_archivos(origen, destino):
    # Obtener la lista de archivos en el directorio de origen
    archivos = os.listdir(origen)

    for archivo in archivos:
        # Construir las rutas completas de origen y destino
        ruta_origen = os.path.join(origen, archivo)
        ruta_destino = os.path.join(destino, archivo)

        # Comprobar si el archivo existe en el directorio de destino
        if os.path.isfile(ruta_destino):
            # Reemplazar el archivo en el directorio de destino
            shutil.copyfile(ruta_origen, ruta_destino)

    print("Archivos restaurados con éxito.")

# Ejemplo de uso
ruta_origen = "./Backup"  # Directorio de origen (respaldo de los archivos originales)
ruta_destino = "./Datos"  # Directorio de destino (archivos que se reemplazarán)

restaurar_archivos(ruta_origen, ruta_destino)
