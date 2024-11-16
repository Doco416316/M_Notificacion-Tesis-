# Importa el módulo de modelos de Django
from django.db import models

class Software(models.Model):
    """
    Modelo que representa el software en el sistema.
    
    Atributos:
        nombre (CharField): Nombre del software.
        version (CharField): Versión del software.
        licencia (CharField): Tipo de licencia del software.
        fecha_instalacion (DateField): Fecha de instalación del software.
    """
    
    # Campo para el nombre del software, con un límite de 100 caracteres
    nombre = models.CharField(max_length=100)
    
    # Campo para la versión del software, con un límite de 50 caracteres
    version = models.CharField(max_length=50)
    
    # Campo para la licencia del software, con un límite de 100 caracteres
    licencia = models.CharField(max_length=100)
    
    # Campo para la fecha de instalación del software
    fecha_instalacion = models.DateField()

    def __str__(self):
        """
        Representa el objeto Software como una cadena, devolviendo su nombre.
        
        :return: str - Nombre del software.
        """
        return self.nombre
