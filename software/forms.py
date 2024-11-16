# Importa el módulo de formularios de Django
from django import forms
# Importa el modelo Software desde el módulo actual
from .models import Software

class SoftwareForm(forms.ModelForm):
    """
    Formulario para crear y editar instancias del modelo Software.

    Este formulario se basa en el modelo Software y permite la 
    entrada de datos para sus campos.
    """
    
    # Define metadatos para el formulario
    class Meta:
        # Especifica el modelo que se utilizará para construir el formulario
        model = Software
        
        # Define los campos del modelo que se incluirán en el formulario
        fields = ['nombre', 'version', 'licencia', 'fecha_instalacion']
