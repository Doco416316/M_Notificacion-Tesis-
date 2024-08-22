# Importa el módulo de modelos de Django
from django.db import models

# Define el modelo Software
class Software(models.Model):
    # Campo para el nombre del software, con un límite de 100 caracteres
    nombre = models.CharField(max_length=100)
    # Campo para la versión del software, con un límite de 50 caracteres
    version = models.CharField(max_length=50)
    # Campo para la licencia del software, con un límite de 100 caracteres
    licencia = models.CharField(max_length=100)
    # Campo para la fecha de instalación del software
    fecha_instalacion = models.DateField()

    # Método para representar el objeto Software como una cadena
    def __str__(self):
        return self.nombre
