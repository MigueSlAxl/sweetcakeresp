# migrate_apps.py
import os
import shutil

carpetas = ['accounts', 'suppliers', 'ventas','ordendetrabajo','productos','ordendecompra','supplies']
subcarpetas = ['__pycache__', 'migrations']

ruta_principal = os.path.dirname(os.path.abspath(__file__))  # Ruta del directorio actual del script

# Recorre las carpetas principales
for carpeta_principal in carpetas:
    # Recorre las subcarpetas
    for subcarpeta in subcarpetas:
        # Construye la ruta completa de la carpeta a eliminar
        ruta_carpeta = os.path.join(ruta_principal, carpeta_principal, subcarpeta)
        
        # Verifica si la carpeta existe y es un directorio
        if os.path.exists(ruta_carpeta) and os.path.isdir(ruta_carpeta):
            # Elimina la carpeta y su contenido de forma recursiva
            shutil.rmtree(ruta_carpeta)
            print(f"Carpeta eliminada: {ruta_carpeta}")
import subprocess

apps = [
    "accounts",
    "admin",
    "auth",
    "authtoken",
    "sessions",
    "contenttypes",
    "productos",
    "suppliers",
    "ordendecompra",
    "supplies",
    "ventas",
    'ordendetrabajo'
]

def migrate_apps():
    for app in apps:
        try:
            subprocess.run(["python", "manage.py", "makemigrations", app], check=True)
            subprocess.run(["python", "manage.py", "migrate", app], check=True)
            print(f"Aplicación {app} migrada correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al migrar la aplicación {app}: {e}")

if __name__ == "__main__":
    migrate_apps()
