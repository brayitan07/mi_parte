# apps/user/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # solo el admin puede asignar roles
    list_display  = ('username', 'email', 'nombre', 'role', 'is_staff')
    list_filter   = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'nombre')
    fieldsets     = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('nombre', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('nombre', 'role')}),
    )

admin.site.register(Role)