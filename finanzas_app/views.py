from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

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

def presupuesto(request):
    return render(request, 'presupuesto.html')
