from django.db import models

class Hardware(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    numero_serie = models.CharField(max_length=100)
    fecha_adquisicion = models.DateField()

    def __str__(self):
        return self.nombre
