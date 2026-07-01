from django.shortcuts import render, redirect, get_object_or_404
from .form import TareasForm, VideoForm, PreguntaForm, ImagenForm
from urllib.parse import urlparse, parse_qs
from .models import (
    Tareas,
    Imagen,
    Pregunta,
    RespuestaCorrecta,
    Opcion,
    RespuestaEstudiante,
)
from django.contrib.auth.decorators import login_required

# Create your views here.


def listar_tareas(request):
    tareas = Tareas.objects.all()
    return render(request, "tareas/listar_tareas.html", {"tareas": tareas})


def crear_tarea(request):

    if request.method == "POST":
        tarea_form = TareasForm(request.POST)
        imagen_form = ImagenForm(request.POST, request.FILES)

        if tarea_form.is_valid() and imagen_form.is_valid():
            # Guardar tarea
            tarea = tarea_form.save()

            # Guardar imagen
            imagen = imagen_form.cleaned_data.get("imagen")

            if imagen:
                Imagen.objects.create(tarea=tarea, imagen=imagen)

            preguntas = request.POST.getlist("preguntas[]")
            tipos = request.POST.getlist("tipos[]")

            respuestas = request.POST.getlist("respuestas[]")

            opcion_a = request.POST.getlist("opcion_a[]")
            opcion_b = request.POST.getlist("opcion_b[]")
            opcion_c = request.POST.getlist("opcion_c[]")
            opcion_d = request.POST.getlist("opcion_d[]")

            correctas = request.POST.getlist("correcta[]")

            for i in range(len(preguntas)):
                if not preguntas[i].strip():
                    continue

                pregunta = Pregunta.objects.create(
                    tarea=tarea, enunciado=preguntas[i], tipo=tipos[i]
                )

                # Pregunta abierta
                if tipos[i] == "texto":
                    RespuestaCorrecta.objects.create(
                        pregunta=pregunta, respuesta=respuestas[i]
                    )

                # Opción múltiple
                elif tipos[i] == "opcion":
                    opciones = {
                        "A": opcion_a[i],
                        "B": opcion_b[i],
                        "C": opcion_c[i],
                        "D": opcion_d[i],
                    }

                    for letra, texto in opciones.items():
                        Opcion.objects.create(
                            pregunta=pregunta,
                            texto=texto,
                            es_correcta=(letra == correctas[i]),
                        )

            return redirect("listar_tareas")

    else:
        tarea_form = TareasForm()
        imagen_form = ImagenForm()

    return render(
        request,
        "tareas/crear_tarea.html",
        {
            "formTarea": tarea_form,
            "formImagen": imagen_form,
        },
    )


def editar_tarea(request, tarea_id):

    tarea = get_object_or_404(Tareas, id=tarea_id)

    if request.method == "POST":
        tarea.titulo = request.POST.get("titulo")
        tarea.descripcion = request.POST.get("descripcion")
        tarea.save()

        preguntas_ids = request.POST.getlist("pregunta_id[]")
        preguntas = request.POST.getlist("preguntas[]")
        tipos = request.POST.getlist("tipos[]")

        for i, pid in enumerate(preguntas_ids):
            pregunta = Pregunta.objects.get(id=pid)

            pregunta.enunciado = preguntas[i]
            pregunta.tipo = tipos[i]
            pregunta.save()

            # si es abierta
            if tipos[i] == "texto":
                pregunta.respuestacorrecta.respuesta = request.POST.getlist(
                    "respuestas[]"
                )[i]
                pregunta.respuestacorrecta.save()

            # si es opción múltiple
            elif tipos[i] == "opcion":
                opciones_ids = request.POST.getlist(f"opcion_id_{pid}[]")
                opciones_textos = request.POST.getlist(f"opcion_texto_{pid}[]")
                correcta = request.POST.get(f"correcta_{pid}")

                for j, oid in enumerate(opciones_ids):
                    op = Opcion.objects.get(id=oid)
                    op.texto = opciones_textos[j]
                    op.es_correcta = str(j + 1) == correcta
                    op.save()

        return redirect("listar_tareas")

    return render(request, "tareas/docente/editar_tarea.html", {"tarea": tarea})


def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)

    if request.method == "POST":
        tarea.delete()
        return redirect("listar_tareas")
    return render(request, "tareas/eliminar_tarea.html", {"tarea": tarea})


def detalle_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)

    resultados = {}
    puntaje_total = 0
    puntaje_obtenido = 0

    if request.method == "POST":
        for pregunta in tarea.preguntas.all():
            respuesta_usuario = request.POST.get(f"pregunta_{pregunta.id}")

            if respuesta_usuario:
                correcta = RespuestaCorrecta.objects.get(pregunta=pregunta)

                es_correcta = (
                    respuesta_usuario.strip().lower()
                    == correcta.respuesta.strip().lower()
                )

                # guardar respuesta
                RespuestaEstudiante.objects.create(
                    pregunta=pregunta,
                    respuesta=respuesta_usuario,
                    es_correcta=es_correcta,
                )

                # resultados para mostrar
                resultados[pregunta.id] = es_correcta

                # puntaje
                puntaje_total += pregunta.puntaje

                if es_correcta:
                    puntaje_obtenido += pregunta.puntaje
            return redirect("listar_tareas")


    return render(
        request,
        "tareas/alumno/detalle_tareas.html",
        {
            "tarea": tarea,
            "resultados": resultados,
            "puntaje_total": puntaje_total,
            "puntaje_obtenido": puntaje_obtenido,
        },
    )


def reproductor(request):

    video_id = None

    if request.method == "POST":
        form = VideoForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data["url"]

            if "watch?v=" in url:
                video_id = url.split("watch?v=")[1].split("&")[0]

    else:
        form = VideoForm()

    return render(
        request, "tareas/reproductor.html", {"form": form, "video_id": video_id}
    )


def subir_imagen(request):
    if request.method == "POST":
        form = ImagenForm(request.POST, request.FILES)

        if form.is_valid():
            tarea = form.cleaned_data["tarea"]
            imagen = form.cleaned_data["imagen"]

            Imagen.objects.create(tarea=tarea, imagen=imagen)

            return redirect("listar_tareas")

    else:
        form = ImagenForm()

    return render(request, "tareas/subir_imagen.html", {"form": form})


def responder_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)

    resultados = {}

    if request.method == "POST":
        for pregunta in tarea.preguntas.all():
            respuesta_usuario = request.POST.get(f"pregunta_{pregunta.id}")

            if respuesta_usuario:
                correcta = RespuestaCorrecta.objects.get(pregunta=pregunta)

                es_correcta = (
                    respuesta_usuario.strip().lower()
                    == correcta.respuesta.strip().lower()
                )

                RespuestaEstudiante.objects.create(
                    pregunta=pregunta,
                    respuesta=respuesta_usuario,
                    es_correcta=es_correcta,
                )

                resultados[pregunta.id] = (
                    "✔ Correcto" if es_correcta else "❌ Incorrecto"
                )

    return render(
        request, "tareas/alumno/detalle_tareas.html", {"tarea": tarea, "resultados": resultados}
    )


def evaluar_respuesta(pregunta, respuesta_usuario):

    if pregunta.tipo == "texto":
        correcta = pregunta.respuestacorrecta.respuesta.lower().strip()

        return respuesta_usuario.lower().strip() == correcta

    elif pregunta.tipo == "opcion":
        return pregunta.opciones.filter(
            texto=respuesta_usuario, es_correcta=True
        ).exists()

    return False


def calcular_nota(tarea, estudiante_respuestas):

    total = 0
    obtenido = 0

    for r in estudiante_respuestas:
        total += r.pregunta.puntaje

        if r.es_correcta:
            obtenido += r.pregunta.puntaje

    return obtenido, total
