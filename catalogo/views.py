from datetime import timedelta, date

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from .models import VideoJuego, UserProfile

def index(request):
    context = {}
    return render(request, 'index.html', context)

def videojuegos(request):
    vj = VideoJuego.objects.select_related('plataforma', 'genero')
    is_vip = getattr(getattr(request.user, 'profile', None), 'vip', False)
    if not is_vip:
        vj = vj.exclude(annio=2026)
    context = { 'videojuegos': vj }
    return render(request, 'videojuegos.html', context)

@login_required
def videojuego_detalle(request, id):
    vj = get_object_or_404(
        VideoJuego.objects.select_related('plataforma', 'genero'),
        pk=id,
    )
    is_vip = getattr(getattr(request.user, 'profile', None), 'vip', False)
    if vj.annio == 2026 and not is_vip:
        messages.error(request, 'Este videojuego es exclusivo para usuarios VIP')
        return redirect('videojuegos')
    context = { 'videojuego': vj }
    return render(request, 'videojuego.html', context)


class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        rut = request.POST.get('rut')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Las contrasenas no coinciden')
            return redirect(reverse('register'))

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Ya existe un usuario con ese email')
            return redirect(reverse('register'))

        if UserProfile.objects.filter(rut=rut).exists():
            messages.error(request, 'Ya existe un usuario con ese RUT')
            return redirect(reverse('register'))

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )
        user.save()

        UserProfile.objects.create(
            user=user,
            rut=rut,
            direccion=direccion,
            telefono=telefono,
        )

        user = authenticate(username=email, password=password1)
        if user is not None:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')

        messages.error(request, 'No se pudo iniciar sesion')
        return redirect(reverse('login'))


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_message = 'Sesion iniciada exitosamente'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contrasena incorrectos')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.WARNING, 'Sesion cerrada exitosamente')
        return response
