
from django.db import models

class Software(models.Model):
    nombre = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    licencia = models.CharField(max_length=100)
    fecha_instalacion = models.DateField()

    def __str__(self):
        return self.nombre
