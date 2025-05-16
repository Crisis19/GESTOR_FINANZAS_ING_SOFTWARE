import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from ..models import Categoria

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

        # Buscar la categoría específica del usuario o una categoría predeterminada
        categoria = Categoria.objects.filter(
            nombre=nombre_categoria
        ).filter(
            Q(usuario_id=request.user.id) | Q(es_predeterminada=True)
        ).first()

        if not categoria:
            messages.error(request, 'La categoría no existe.')
            return redirect('categorias')

        # Actualizar el monto máximo
        categoria.monto_max = monto_maximo
        categoria.save()
        messages.success(request, 'Monto máximo definido con éxito.')
        return redirect('categorias')

    return redirect('categorias')

def consultar_categoria(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    return render(request, 'categoria.html', {'categorias': categorias})
