from django import forms
from .models import Nota

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['estudiante', 'materia', 'calificacion']
        widgets = {
            'estudiante': forms.TextInput(attrs={'class': 'form-control'}),
            'materia': forms.TextInput(attrs={'class': 'form-control'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control'}),
        }