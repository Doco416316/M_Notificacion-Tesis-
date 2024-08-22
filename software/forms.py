# Importa el módulo de formularios de Django
from django import forms
# Importa el modelo Software desde el módulo actual
from .models import Software

# Define un formulario basado en el modelo Software
class SoftwareForm(forms.ModelForm):
    # Define metadatos para el formulario
    class Meta:
        # Especifica el modelo que se utilizará para construir el formulario
        model = Software
        # Define los campos del modelo que se incluirán en el formulario
        fields = ['nombre', 'version', 'licencia', 'fecha_instalacion']
