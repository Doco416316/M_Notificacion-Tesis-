# Importa el módulo models de Django, que proporciona una serie de clases para definir los modelos de la aplicación
from django.db import models

# Define un modelo llamado Hardware, que representa la información del hardware en la base de datos
class Hardware(models.Model):
    # Campo nombre: Un campo de texto con un tamaño máximo de 100 caracteres para almacenar el nombre del hardware
    nombre = models.CharField(max_length=100)
    
    # Campo marca: Un campo de texto con un tamaño máximo de 50 caracteres para almacenar la marca del hardware
    marca = models.CharField(max_length=50)
    
    # Campo modelo: Un campo de texto con un tamaño máximo de 50 caracteres para almacenar el modelo del hardware
    modelo = models.CharField(max_length=50)
    
    # Campo numero_serie: Un campo de texto con un tamaño máximo de 100 caracteres para almacenar el número de serie del hardware
    numero_serie = models.CharField(max_length=100)
    
    # Campo fecha_adquisicion: Un campo de fecha para almacenar la fecha de adquisición del hardware
    fecha_adquisicion = models.DateField()

    # Método __str__: Devuelve el nombre del hardware cuando se convierte el objeto a una cadena (por ejemplo, en el panel de administración)
    def __str__(self):
        return self.nombre
