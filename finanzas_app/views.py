from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Transaccion, Categoria

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
    categorias = Categoria.objects.filter(usuario=request.user)
    return render(request, 'categoria.html', {'categorias': categorias})

def presupuesto(request):
    return render(request, 'presupuesto.html')
