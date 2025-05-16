from django.urls import path
from . import views
from .model import login, categoria

urlpatterns = [
    path('', views.login_view, name='login'),
    path('singin/', login.registro, name='singin'),
    path('cerrar_sesion/', login.cerrar_sesion, name='cerrar_sesion'),
    path('login/', login.iniciar_sesion),
    path('home/', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('añadir/', views.añadir, name='añadir'),
    path('quitar/', views.quitar, name='quitar'),
    path('metas/', views.metas, name='metas'),
    path('presupuesto/', views.presupuesto, name='presupuesto'),
    path('categorias/', views.categoria, name='categorias'),
    path('crear_categoria/', categoria.crear_categoria, name='crear_categoria'),
    path('definir_monto_maximo/', categoria.definir_monto_maximo, name='definir_monto_maximo'),
    path('transacciones/', views.transacciones, name='transacciones'),
    path('graficos/', views.graficos, name='graficos'),
]
