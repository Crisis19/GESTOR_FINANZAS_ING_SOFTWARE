from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum, Q
from .models import Transaccion, Categoria
from .models import TransaccionForm

@login_required
def home(request):
    usuario = request.user
    hoy = timezone.now()
    mes_actual = hoy.month
    anio_actual = hoy.year

    # Filtrar transacciones del mes actual
    transacciones_mes = Transaccion.objects.filter(
        usuario=usuario,
        fecha__year=anio_actual,
        fecha__month=mes_actual
    )

    # Calcular ingresos y gastos
    ingresos = sum(t.monto for t in transacciones_mes if t.tipo == 'ingreso')
    gastos = sum(t.monto for t in transacciones_mes if t.tipo == 'gasto')
    balance = ingresos - gastos

    contexto = {
        'ingresos': ingresos,
        'gastos': gastos,
        'balance': balance,
        'transacciones_mes': transacciones_mes,
    }

    return render(request, 'home.html', contexto)

def login_view(request):
    return render(request, 'login.html')

def registro(request):
    return render(request, 'registro.html')

def añadir(request):
    return render(request, 'añadir.html')

def quitar(request):
    return render(request, 'quitar.html')

def metas(request):
    return render(request, 'metas.html')

def categoria(request):
    categorias = Categoria.objects.filter(usuario=request.user | Q(es_predeterminada=True))
    return render(request, 'categoria.html', {'categorias': categorias})

def presupuesto(request):
    return render(request, 'presupuesto.html')

def transaccion(request):
    return render(request, 'transacciones.html')

def transacciones(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user
            transaccion.save()
            messages.success(request, 'Transacción guardada con éxito.')
            return redirect('transacciones')
    else:
        form = TransaccionForm()

    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'transacciones.html', {'form': form, 'transacciones': transacciones})

def datos_graficos(request):
    # Datos para la gráfica de pastel
    gastos_por_categoria = (
        Transaccion.objects.filter(usuario=request.user, tipo='gasto')
        .values('categoria__nombre')  # Accede al nombre de la categoría relacionada
        .annotate(total=Sum('monto'))
    )

    # Datos para la gráfica de barras
    ingresos = Transaccion.objects.filter(usuario=request.user, tipo='ingreso').aggregate(total=Sum('monto'))['total'] or 0
    gastos = Transaccion.objects.filter(usuario=request.user, tipo='gasto').aggregate(total=Sum('monto'))['total'] or 0

    return JsonResponse({
        'gastos_por_categoria': list(gastos_por_categoria),
        'ingresos': ingresos,
        'gastos': gastos,
    })
