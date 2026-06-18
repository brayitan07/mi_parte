from django import forms
from .models import Tareas, Pregunta, Imagen


class TareasForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ["titulo", "descripcion", "video", "fecha_entrega"]

        widgets = {"fecha_entrega": forms.DateInput(attrs={"type": "date"})}

class ImagenForm(forms.ModelForm):

    class Meta:
        model = Imagen
        fields = ["imagen"]


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = [
            'enunciado',
            'tipo'
        ]


class VideoForm(forms.Form):
    url = forms.URLField(label="URL de YouTube")
