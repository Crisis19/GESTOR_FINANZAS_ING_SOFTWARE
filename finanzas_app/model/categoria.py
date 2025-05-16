import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from ..models import Categoria, UsuarioCategoria

@csrf_exempt
def crear_categoria(request):
    if request.method == 'POST':
        try:
            # Procesar el cuerpo de la solicitud como JSON
            data = json.loads(request.body)
            nombre = data.get('nombre')
            es_predeterminada = data.get('es_predeterminada', False)
            usuario = request.user

            # Verificar si la categoría ya existe
            if Categoria.objects.filter(nombre=nombre, usuario=usuario).exists():
                return JsonResponse({'error': 'La categoría ya existe.'}, status=400)

            # Crear la nueva categoría
            categoria = Categoria(nombre=nombre, es_predeterminada=es_predeterminada, usuario=usuario)
            categoria.save()
            return JsonResponse({'mensaje': 'Categoría creada con éxito.'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido.'}, status=400)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def definir_monto_maximo(request):
    if request.method == 'POST':
        nombre_categoria = request.POST.get('categoria')
        monto_maximo = request.POST.get('monto-maximo')

        # Buscar la categoría
        categoria = Categoria.objects.filter(nombre=nombre_categoria).first()

        if not categoria:
            messages.error(request, 'La categoría no existe.')
            return redirect('categorias')

        # Buscar o crear la relación UsuarioCategoria
        usuario_categoria, created = UsuarioCategoria.objects.get_or_create(
            usuario=request.user,
            categoria=categoria
        )

        # Actualizar el monto máximo
        usuario_categoria.monto_max = monto_maximo
        usuario_categoria.save()
        messages.success(request, 'Monto máximo definido con éxito.')
        return redirect('categorias')

    return redirect('categorias')

def consultar_categoria(request):
    usuario_categorias = UsuarioCategoria.objects.filter(usuario=request.user).select_related('categoria')
    return render(request, 'categoria.html', {'usuario_categorias': usuario_categorias})
