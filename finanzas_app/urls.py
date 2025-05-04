from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('añadir/', views.añadir, name='añadir'),
    path('quitar/', views.quitar, name='quitar'),
    path('metas/', views.metas, name='metas'),
    path('presupuesto/', views.presupuesto, name='presupuesto'),
]
