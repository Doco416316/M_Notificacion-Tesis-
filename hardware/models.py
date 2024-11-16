# Importa el módulo models de Django, que proporciona una serie de clases para definir los modelos de la aplicación
from django.db import models

# Define un modelo llamado Hardware, que representa la información del hardware en la base de datos
class Hardware(models.Model):
    # Campo nombre: Almacena el nombre del hardware, con un tamaño máximo de 100 caracteres
    nombre = models.CharField(max_length=100)
    
    # Campo marca: Almacena la marca del hardware, con un tamaño máximo de 50 caracteres
    marca = models.CharField(max_length=50)
    
    # Campo modelo: Almacena el modelo del hardware, con un tamaño máximo de 50 caracteres
    modelo = models.CharField(max_length=50)
    
    # Campo numero_serie: Almacena el número de serie del hardware, con un tamaño máximo de 100 caracteres
    numero_serie = models.CharField(max_length=100)
    
    # Campo fecha_adquisicion: Almacena la fecha de adquisición del hardware
    fecha_adquisicion = models.DateField()

    # Método __str__: Devuelve el nombre del hardware cuando se convierte el objeto a una cadena
    def __str__(self):
        return self.nombre
