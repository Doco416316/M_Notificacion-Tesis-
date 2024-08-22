# Importa el módulo de formularios de Django
from django import forms
# Importa el modelo Hardware desde el archivo models.py en la misma aplicación
from .models import Hardware

# Define un formulario para el modelo Hardware usando ModelForm
class HardwareForm(forms.ModelForm):
    class Meta:
        # Especifica que este formulario está asociado con el modelo Hardware
        model = Hardware
        # Define los campos del modelo que serán incluidos en el formulario
        fields = ['nombre', 'marca', 'modelo', 'numero_serie', 'fecha_adquisicion']
