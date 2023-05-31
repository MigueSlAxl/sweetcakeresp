# migrate_apps.py

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
