from django.contrib.auth import get_user_model
from catalogo.models import Videojuego

User = get_user_model()

# =========================
# CREAR SUPERUSUARIO
# =========================
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password="12345"
    )
    print("Superusuario creado")
else:
    print("Superusuario ya existe")


# =========================
# CREAR DATOS DE PRUEBA
# =========================
if Videojuego.objects.count() == 0:
    Videojuego.objects.create(nombre="GTA V", descripcion="Juego de mundo abierto")
    Videojuego.objects.create(nombre="FIFA 24", descripcion="Juego de fútbol")
    Videojuego.objects.create(nombre="Call of Duty", descripcion="Shooter")
    print("Datos de prueba creados")
else:
    print("Ya hay videojuegos cargados")