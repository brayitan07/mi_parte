from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('iniciar/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('cerrar/', views.cerrar_sesion, name='cerrar_sesion'),
    path('inicio/', views.inicio, name='inicio'),
    path('', views.inicio, name='index'),
    path('redireccion/', views.redireccion_usuario, name='redireccion_usuario'),
    path('panel-usuario/', views.panel_usuario, name='panel_usuario'),
    path('prescolar/', views.prescolar, name='prescolar'),
    path('primaria/', views.primaria, name='primaria'),
    path('segundaria/', views.segundaria, name='segundaria'),
    path('feria-ciencia/', views.feria_ciencia, name='feria_ciencia'),
    path('festival-artistico/', views.festival_artistico, name='festival_artistico'),
    path('semana-lectura/', views.semana_lectura, name='semana_lectura'),
    # Panel Admin
path('admin-panel/',         views.panel_admin,          name='panel_admin'),
path('admin-panel/usuarios/', views.admin_usuarios,       name='admin_usuarios'),
path('admin-panel/usuarios/<int:user_id>/toggle/', views.admin_toggle_usuario, name='admin_toggle_usuario'),
path('admin-panel/tareas/',   views.admin_tareas,         name='admin_tareas'),
path('admin-panel/estudiantes/', views.admin_estudiantes, name='admin_estudiantes'),
path('admin-panel/docentes/', views.admin_docentes,       name='admin_docentes'),

    # Recuperar contraseña
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='user/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='user/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='user/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='user/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]