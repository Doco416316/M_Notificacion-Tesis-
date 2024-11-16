from django.db import models
from django.conf import settings
from django.utils import timezone
import joblib
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Modelo para representar información del hardware
class Hardware(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    numero_serie = models.CharField(max_length=100)
    fecha_adquisicion = models.DateField()
    def __str__(self):
        return self.nombre

# Modelo para representar información del software
class Software(models.Model):
    nombre = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    licencia = models.CharField(max_length=50)
    fecha_instalacion = models.DateField()
    def __str__(self):
        return self.nombre

# Modelo para las notificaciones generadas en el sistema
class Notificacion(models.Model):
    # Definición de prioridades para notificaciones
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),]
    # Campos de la notificación
    mensaje = models.TextField()
    prioridad = models.CharField(max_length=5, choices=PRIORIDAD_CHOICES, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    # Tipos de cambio que pueden originar una notificación
    TIPO_CAMBIO_CHOICES = [
        ('agregar', 'Agregar'),
        ('modificar', 'Modificar'),
        ('eliminar', 'Eliminar'),]
    tipo_cambio = models.CharField(max_length=10, choices=TIPO_CAMBIO_CHOICES, default='agregar')
    origen = models.CharField(max_length=50, default='software')
    # Relaciones opcionales a modelos Hardware y Software
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, null=True, blank=True)
    software = models.ForeignKey(Software, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para predecir la prioridad de la notificación
        si esta no está definida.
        """
        if not self.prioridad:
            self.prioridad = self.predecir_prioridad()
        super().save(*args, **kwargs)

    def predecir_prioridad(self):
        """
        Utiliza un modelo preentrenado para predecir la prioridad de la notificación.
        Retorna 'alta', 'media' o 'baja' según la predicción.
        """
        # Cargar el modelo de prioridad
        modelo_path = os.path.join(settings.BASE_DIR, 'm_prioridad.pkl')
        modelo_prioridad = joblib.load(modelo_path)
        # Codificación de los datos para el modelo
        tipo_cambio_encoder = LabelEncoder().fit(['agregar', 'modificar', 'eliminar'])
        tipo_cambio_encoded = tipo_cambio_encoder.transform([self.tipo_cambio])[0]
        origen_encoded = 1 if self.origen == 'hardware' else 0  # Codificación binaria para el origen
        # Crear DataFrame para la predicción
        data = pd.DataFrame({
            'Leido': [self.leido],
            'Tipo de Cambio': [tipo_cambio_encoded],
            'Origen': [origen_encoded],})
        data = data[['Leido', 'Tipo de Cambio', 'Origen']]
        # Imprimir los datos procesados para depuración
        print("Datos para predicción:", data)
        # Realizar la predicción y mapear el resultado
        prioridad_predicha_num = modelo_prioridad.predict(data)[0]
        prioridad_mapeo = {0: 'alta', 1: 'baja', 2: 'media'}
        return prioridad_mapeo.get(prioridad_predicha_num, 'baja')
    def __str__(self):
        return f"{self.prioridad} - {self.fecha_creacion}"

# Modelo para almacenar notificaciones eliminadas
class NotificacionEliminada(models.Model):
    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE)
    fecha_eliminacion = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.notificacion.mensaje} - Eliminada en {self.fecha_eliminacion}"

# Modelo para registrar modificaciones de prioridad de las notificaciones
class NotificacionModificada(models.Model):
    notificacion = models.ForeignKey('Notificacion', on_delete=models.CASCADE)
    prioridad_anterior = models.CharField(max_length=10, choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')])
    nueva_prioridad = models.CharField(max_length=10, choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')])
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Notificación modificada: {self.notificacion.id} - {self.fecha_modificacion}"
