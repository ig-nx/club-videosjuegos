from django.db import models
from django.contrib.auth.models import User

class Plataforma(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    imagen = models.CharField(max_length=255, blank = True, null = True)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
class VideoJuego(models.Model):
    titulo = models.CharField(max_length=255, blank = False, null = False)
    descripcion = models.TextField()
    annio = models.PositiveIntegerField()
    imagen = models.CharField(max_length=255, blank = True, null = True)

    plataforma = models.ForeignKey(
        Plataforma,
        on_delete=models.PROTECT,
        related_name='videojuegos'
    )

    genero = models.ForeignKey(
        Genero,
        on_delete=models.PROTECT,
        related_name='videojuegos' # related_name es para poder acceder a la lista de videojuegos de un genero
    )

    def __str__(self):
        return f'{self.titulo} ({self.annio})' # El __str__ es para que al imprimir un videojuego se muestre el titulo y el año, en lugar de la referencia al objeto

class UserProfile(models.Model):
    
    rut = models.CharField(max_length=12, unique=True, blank=False, null=False)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    vip = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') # OneToOneField es para que cada usuario tenga un perfil unico, y related_name es para poder acceder al perfil de un usuario desde el objeto User

    def __str__(self):
        id = self.user.id
        nombre = self.user.first_name
        apellido = self.user.last_name
        usuario = self.user.username
        rut = self.rut
        return f'{id} - {nombre} {apellido} ({usuario}) - RUT: {rut}'