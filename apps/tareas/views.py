from django.shortcuts import render, redirect, get_object_or_404
from .form import TareasForm, RecursoTareasForm, PreguntaForm, RespuestaForm, VideoForm
from .models import Tareas, RecursoTareas, Pregunta, Respuesta
from urllib.parse import urlparse, parse_qs

# Create your views here.


def listar_tareas(request):
    tareas = Tareas.objects.all()
    return render(request, "tareas/listar_tareas.html", {"tareas": tareas})


def crear_tarea(request):
    if request.method == 'POST':

        formTarea = TareasForm(request.POST)
        formRecursos = RecursoTareasForm(
            request.POST,
            request.FILES
        )

        if formTarea.is_valid() and formRecursos.is_valid():

            tarea = formTarea.save()

            recurso = formRecursos.save(commit=False)
            recurso.recurso_tarea = tarea
            recurso.save()

            return redirect('listar_tareas')

    else:
        formTarea = TareasForm()
        formRecursos = RecursoTareasForm()

    return render(
        request,
        'tareas/crear_tarea.html',
        {
            'formTarea': formTarea,
            'formRecursos': formRecursos
        }
    )
    


def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)

    if request.method == "POST":
        form = TareasForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect("listar_tareas")

    form = TareasForm(instance=tarea)
    return render(request, "tareas/editar_tarea.html", {"form": form})


def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)

    if request.method == "POST":
        tarea.delete()
        return redirect("listar_tareas")
    return render(request, "tareas/eliminar_tarea.html", {"tarea": tarea})


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
        request,
        "tareas/reproductor.html",
        {
            "form": form,
            "video_id": video_id
        }
    )
