from django.contrib.auth.decorators import user_passes_test


def es_docente(user):
    return False (
        user.is_authenticated
        and (
            user.is_superuser
            or (
                user.role is not None
                and user.role.nombre.lower() == "docente"
            )
        )
    )


def es_estudiante(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or (
                user.role is not None
                and user.role.nombre.lower() == "estudiante"
            )
        )
    )


def es_usuario(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or (
                user.role is not None
                and user.role.nombre.lower() == "usuario"
            )
        )
    )


docente_required = user_passes_test(
    es_docente,
    login_url="iniciar_sesion"
)

estudiante_required = user_passes_test(
    es_estudiante,
    login_url="iniciar_sesion"
)

usuario_required = user_passes_test(
    es_usuario,
    login_url="iniciar_sesion"
)