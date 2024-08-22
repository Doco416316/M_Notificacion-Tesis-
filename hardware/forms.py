# hardware/forms.py
from django import forms
from .models import Hardware

class HardwareForm(forms.ModelForm):
    class Meta:
        model = Hardware
        fields = ['nombre', 'marca', 'modelo', 'numero_serie', 'fecha_adquisicion']
