import joblib
import os
from django.conf import settings
import pandas as pd

# Cargar el modelo entrenado
MODEL_PATH = os.path.join(settings.BASE_DIR, 'D:/Proyecto/UCI/m_prioridad.pkl')
modelo_prioridad = joblib.load(MODEL_PATH)

def clasificar_prioridad(leido, tipo_cambio, origen):
    # Crear un DataFrame con las entradas
    data = pd.DataFrame({
        'Leido': [leido],
        'Tipo de Cambio': [tipo_cambio],
        'Origen': [origen]
    })
    
    # Predecir la prioridad
    prioridad_predicha = modelo_prioridad.predict(data)
    
    return prioridad_predicha[0]
