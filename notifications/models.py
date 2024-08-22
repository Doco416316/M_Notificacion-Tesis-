from django.db import models  # Importa el módulo models de Django, necesario para definir modelos de base de datos.
import joblib  # Importa joblib, usado para cargar y guardar modelos de machine learning.
import os  # Importa os, que permite interactuar con el sistema operativo, como manejar rutas de archivos.
from django.conf import settings  # Importa el objeto settings de Django, que contiene la configuración del proyecto.
import pandas as pd  # Importa pandas, una librería para manipulación y análisis de datos.
from sklearn.preprocessing import LabelEncoder  # Importa LabelEncoder, usado para convertir valores categóricos en números.

class Notificacion(models.Model):
    # Define las opciones de prioridad que puede tener una notificación.
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    # Campos del modelo Notificacion
    mensaje = models.TextField()  # Campo para almacenar el mensaje de la notificación.
    prioridad = models.CharField(max_length=5, choices=PRIORIDAD_CHOICES, blank=True)  # Prioridad con opciones limitadas.
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación, se asigna automáticamente al guardar.
    leido = models.BooleanField(default=False)  # Indica si la notificación ha sido leída.

    # Define las opciones de tipo de cambio que puede haber en una notificación.
    TIPO_CAMBIO_CHOICES = [
        ('agregar', 'Agregar'),
        ('modificar', 'Modificar'),
        ('eliminar', 'Eliminar'),
    ]
    tipo_cambio = models.CharField(max_length=10, choices=TIPO_CAMBIO_CHOICES, default='agregar')  # Tipo de cambio.
    origen = models.CharField(max_length=50, default='software')  # Origen del cambio, puede ser 'software' o 'hardware'.

    def save(self, *args, **kwargs):
        # Solo calcular la prioridad si no ha sido definida manualmente.
        if not self.prioridad:
            self.prioridad = self.predecir_prioridad()  # Llama al método predecir_prioridad si no hay prioridad definida.
        super().save(*args, **kwargs)  # Guarda el objeto Notificacion en la base de datos.

    def predecir_prioridad(self):
        # Cargar el modelo entrenado desde la ruta especificada.
        modelo_path = os.path.join(settings.BASE_DIR, 'D:/Proyecto/UCI/m_prioridad.pkl')
        modelo_prioridad = joblib.load(modelo_path)

        # Entrena un LabelEncoder con las mismas categorías que se usaron para entrenar el modelo.
        tipo_cambio_encoder = LabelEncoder().fit(['agregar', 'modificar', 'eliminar'])
        tipo_cambio_encoded = tipo_cambio_encoder.transform([self.tipo_cambio])[0]  # Codifica el tipo de cambio actual.

        # Codificación del campo 'origen', donde 'hardware' es 1 y 'software' es 0.
        origen_encoded = 1 if self.origen == 'hardware' else 0

        # Crear un DataFrame con los valores numéricos para la predicción.
        data = pd.DataFrame({
            'Leido': [self.leido],  # Valor de si la notificación ha sido leída o no.
            'Tipo de Cambio': [tipo_cambio_encoded],  # Tipo de cambio codificado.
            'Origen': [origen_encoded],  # Origen codificado.
        })
        data = data[['Leido', 'Tipo de Cambio', 'Origen']]  # Ordena las columnas del DataFrame.

        # Imprimir los datos para depuración (esto es útil para verificar lo que se está pasando al modelo).
        print("Datos para predicción:", data)

        # Utiliza el modelo cargado para predecir la prioridad basada en los datos.
        prioridad_predicha_num = modelo_prioridad.predict(data)[0]

        # Mapear la prioridad numérica a su representación categórica en el modelo.
        prioridad_mapeo = {0: 'alta', 1: 'baja', 2: 'media'}  # Diccionario de mapeo de valores numéricos a prioridades.
        prioridad_predicha = prioridad_mapeo.get(prioridad_predicha_num, 'baja')  # Devuelve la prioridad predicha.

        return prioridad_predicha  # Retorna la prioridad predicha.

    def __str__(self):
        # Representa el objeto Notificacion como una cadena, mostrando la prioridad y la fecha de creación.
        return f"{self.prioridad} - {self.fecha_creacion}"
