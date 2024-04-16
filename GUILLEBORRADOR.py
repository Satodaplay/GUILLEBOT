import os

def borrar_archivo(ruta):
    try:
        os.remove(ruta)
        print(f"El archivo {ruta} ha sido eliminado correctamente.")
    except FileNotFoundError:
        print(f"El archivo {ruta} no fue encontrado.")
    except PermissionError:
        print(f"No tienes permisos para borrar el archivo {ruta}.")
    except Exception as e:
        print(f"Ocurrió un error al intentar borrar el archivo {ruta}: {e}")

# Ejemplo de uso
archivo_a_borrar = r"audio.mp4"  # Coloca la ruta del archivo que quieres borrar aquí
borrar_archivo(archivo_a_borrar)
