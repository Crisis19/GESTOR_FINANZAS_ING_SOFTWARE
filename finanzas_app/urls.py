from django.urls import path
from . import views
from .model import login

urlpatterns = [
    path('', views.login_view, name='login'),
    path('singin/', login.registro, name='singin'),
    path('login/', login.iniciar_sesion),
    path('home/', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('añadir/', views.añadir, name='añadir'),
    path('quitar/', views.quitar, name='quitar'),
    path('metas/', views.metas, name='metas'),
    path('presupuesto/', views.presupuesto, name='presupuesto'),
    path('categorias/', views.categoria, name='categorias'),
]
