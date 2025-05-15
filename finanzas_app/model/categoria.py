from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from ..models import Categoria
def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        monto_max = request.POST.get('monto_max')
        es_predeterminada = request.POST.get('es_predeterminada', False)
        usuario = request.user

        # Verificar si la categoría ya existe
        if Categoria.objects.filter(nombre=nombre, usuario=usuario).exists():
            messages.error(request, 'La categoría ya existe.')
            return redirect('categorias')

        # Crear la nueva categoría
        categoria = Categoria(nombre=nombre, monto_max=monto_max, es_predeterminada=es_predeterminada, usuario=usuario)
        categoria.save()
        messages.success(request, 'Categoría creada con éxito.')
        return redirect('categorias')

    return render(request, 'categoria.html')

def consultar_categoria(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    return render(request, 'consultar_categoria.html', {'categorias': categorias})
