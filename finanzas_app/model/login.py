from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from ..models import PerfilUsuario

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        moneda = request.POST.get('moneda_predeterminada', 'COP')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return render(request, 'usuarios/registro.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        PerfilUsuario.objects.create(user=user, moneda_predeterminada=moneda)

        login(request, user)
        return redirect('home')

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige a la página principal
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('login')  # Redirige a la página de inicio de sesión
def cambiar_contrasena(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Contraseña cambiada con éxito.')
            return redirect('login')  # Redirige a la página de inicio de sesión
        else:
            messages.error(request, 'La contraseña actual es incorrecta.')

    return render(request, 'usuarios/cambiar_contrasena.html')
