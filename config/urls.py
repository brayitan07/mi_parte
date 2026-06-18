from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Allauth
    path('accounts/', include('allauth.urls')),

    path('docente/', include('apps.docente.urls')),
    path('', include('apps.tareas.urls')),
    path('', include('apps.user.urls')),
    path('alumno/', include('apps.alumno.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
