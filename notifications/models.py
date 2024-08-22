from django.db import models
import joblib
import os
from django.conf import settings
import pandas as pd
from sklearn.preprocessing import LabelEncoder

class Notificacion(models.Model):
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    mensaje = models.TextField()
    prioridad = models.CharField(max_length=5, choices=PRIORIDAD_CHOICES, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    TIPO_CAMBIO_CHOICES = [
        ('agregar', 'Agregar'),
        ('modificar', 'Modificar'),
        ('eliminar', 'Eliminar'),
    ]
    tipo_cambio = models.CharField(max_length=10, choices=TIPO_CAMBIO_CHOICES, default='agregar')
    origen = models.CharField(max_length=50, default='software')  # Puede ser 'software' o 'hardware'

    def save(self, *args, **kwargs):
        # Solo calcular la prioridad si no ha sido definida manualmente
        if not self.prioridad:
            self.prioridad = self.predecir_prioridad()
        super().save(*args, **kwargs)

    def predecir_prioridad(self):
        modelo_path = os.path.join(settings.BASE_DIR, 'D:/Proyecto/UCI/m_prioridad.pkl')
        modelo_prioridad = joblib.load(modelo_path)

        # Asegúrate de que LabelEncoder está entrenado con las mismas categorías
        tipo_cambio_encoder = LabelEncoder().fit(['agregar', 'modificar', 'eliminar'])
        tipo_cambio_encoded = tipo_cambio_encoder.transform([self.tipo_cambio])[0]

        # Codificación del campo 'origen'
        origen_encoded = 1 if self.origen == 'hardware' else 0

        # Crear un DataFrame con los valores numéricos
        data = pd.DataFrame({
            'Leido': [self.leido],
            'Tipo de Cambio': [tipo_cambio_encoded],
            'Origen': [origen_encoded],
        })
        data = data[['Leido', 'Tipo de Cambio', 'Origen']]

        # Imprimir los datos para depuración
        print("Datos para predicción:", data)

        # Predecir prioridad numérica
        prioridad_predicha_num = modelo_prioridad.predict(data)[0]

        # Mapear la prioridad numérica a la correspondiente en el modelo
        prioridad_mapeo = {0: 'alta', 1: 'baja', 2: 'media'}
        prioridad_predicha = prioridad_mapeo.get(prioridad_predicha_num, 'baja')

        return prioridad_predicha

    def __str__(self):
        return f"{self.prioridad} - {self.fecha_creacion}"
