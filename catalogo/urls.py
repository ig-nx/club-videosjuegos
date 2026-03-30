from django.urls import path
from .views import (
    index,
    videojuegos,
    videojuego_detalle,
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
)

urlpatterns = [
    path('', index, name='index'),
    path('videojuegos/', videojuegos, name='videojuegos'),
    path('videojuego/<int:id>/', videojuego_detalle, name='videojuego'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
