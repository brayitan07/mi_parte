from django import forms
from .models import Tareas, RecursoTareas, Pregunta, Respuesta

class TareasForm(forms.ModelForm):    
    class Meta:
        model = Tareas
        fields = ['titulo', 'descripcion', 'fecha_entrega']
        widgets = {
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
        }


class RecursoTareasForm(forms.ModelForm):
    class Meta:
        model = RecursoTareas
        fields = ['tipo', 'archivo', 'url']


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['enunciado', 'tipo']

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['respuesta_texto', 'opcion_seleccionada']


class VideoForm(forms.Form):
    url = forms.URLField(
        label="URL de YouTube"
    )