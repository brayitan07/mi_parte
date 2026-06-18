from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='index'),
    path('iniciar/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('cerrar/', views.cerrar_sesion, name='cerrar_sesion'),
    path('inicio/', views.inicio, name='inicio'),
]