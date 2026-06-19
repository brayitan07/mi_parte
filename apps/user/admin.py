from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "Información adicional",
            {
                "fields": (
                    "nombre",
                    "role",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "nombre",
        "role",
        "is_staff",
    )


admin.site.register(Role)