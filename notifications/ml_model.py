import joblib  # Importa la librería joblib, usada para cargar y guardar modelos de machine learning.
import os  # Importa la librería os, que permite interactuar con el sistema operativo, como para manejar rutas de archivos.
from django.conf import settings  # Importa el objeto settings de Django, que contiene la configuración del proyecto.
import pandas as pd  # Importa pandas, una librería para manipulación y análisis de datos.

# Cargar el modelo entrenado
# Define la ruta completa al archivo del modelo utilizando os.path.join para asegurar compatibilidad con diferentes sistemas operativos.
MODEL_PATH = os.path.join(settings.BASE_DIR, 'D:/Proyecto/UCI/m_prioridad.pkl')

# Carga el modelo de machine learning previamente entrenado desde el archivo especificado.
modelo_prioridad = joblib.load(MODEL_PATH)

def clasificar_prioridad(leido, tipo_cambio, origen):
    # Crear un DataFrame con las entradas
    # Crea un DataFrame de pandas con las características requeridas para la predicción.
    data = pd.DataFrame({
        'Leido': [leido],  # Valor de si la notificación ha sido leída o no.
        'Tipo de Cambio': [tipo_cambio],  # Tipo de cambio (ej: agregar, modificar, eliminar).
        'Origen': [origen]  # Origen del cambio (ej: hardware, software).
    })
    
    # Predecir la prioridad
    # Usa el modelo cargado para predecir la prioridad basándose en los datos proporcionados.
    prioridad_predicha = modelo_prioridad.predict(data)
    
    # Retornar la prioridad predicha
    # Devuelve la primera (y única) predicción realizada por el modelo, que representa la prioridad clasificada.
    return prioridad_predicha[0]
