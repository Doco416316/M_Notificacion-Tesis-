import joblib  # Para cargar y guardar el modelo.
import os  # Para manejo de rutas.
from django.conf import settings  # Configuraciones de Django.
import pandas as pd  # Para crear DataFrames.
from sklearn.linear_model import SGDClassifier  # Modelo que soporta entrenamiento incremental.

# Ruta donde se guarda el modelo
MODEL_PATH = os.path.join(settings.BASE_DIR, '../m_prioridad.pkl')

<<<<<<< HEAD
def cargar_o_inicializar_modelo():
    """
    Carga el modelo de clasificación si existe, o inicializa un nuevo modelo si no.
    Retorna el modelo de clasificación.
    """
    if os.path.exists(MODEL_PATH):
        modelo_prioridad = joblib.load(MODEL_PATH)  # Carga el modelo existente.
    else:
        modelo_prioridad = SGDClassifier()  # Inicializa un nuevo modelo.
    return modelo_prioridad

# Cargar el modelo al iniciar el módulo
modelo_prioridad = cargar_o_inicializar_modelo()
=======
# Función para cargar o inicializar el modelo
def cargar_o_inicializar_modelo():
    if os.path.exists(MODEL_PATH):
        # Si el modelo existe, lo cargamos
        modelo_prioridad = joblib.load(MODEL_PATH)
    else:
        # Si el modelo no existe, inicializamos un nuevo modelo que soporte entrenamiento incremental
        modelo_prioridad = SGDClassifier()
    return modelo_prioridad
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4

# Cargar el modelo
modelo_prioridad = cargar_o_inicializar_modelo()

# Función para clasificar la prioridad de una notificación
def clasificar_prioridad(leido, tipo_cambio, origen):
    """
    Clasifica la prioridad de una notificación basándose en su estado leído,
    tipo de cambio y origen. Retorna la prioridad predicha.
    """
    # Crear un DataFrame con las entradas
    data = pd.DataFrame({
        'Leido': [leido],
        'Tipo de Cambio': [tipo_cambio],
<<<<<<< HEAD
        'Origen': [origen]})
    # Predecir la prioridad utilizando el modelo
    prioridad_predicha = modelo_prioridad.predict(data)
    return prioridad_predicha[0]  # Retorna la prioridad predicha

def entrenar_con_nueva_notificacion(leido, tipo_cambio, origen, prioridad):
    """
    Entrena el modelo con una nueva notificación. 
    Utiliza la nueva entrada para actualizar el modelo y guarda los cambios.
    :param leido: Estado leído de la notificación (True/False).
    :param tipo_cambio: Tipo de cambio (e.g., 'agregar', 'modificar', 'eliminar').
    :param origen: Origen de la notificación (e.g., 'software', 'hardware').
    :param prioridad: Prioridad de la notificación ('alta', 'media', 'baja').
    """
    global modelo_prioridad  # Usamos el modelo cargado globalmente.
=======
        'Origen': [origen]
    })

    # Predecir la prioridad
    prioridad_predicha = modelo_prioridad.predict(data)

    # Retornar la prioridad predicha
    return prioridad_predicha[0]

# Función para entrenar el modelo con una nueva notificación
def entrenar_con_nueva_notificacion(leido, tipo_cambio, origen, prioridad):
    global modelo_prioridad  # Usamos el modelo cargado globalmente.

>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
    # Crear el DataFrame de entrenamiento con la nueva notificación
    X_nueva = pd.DataFrame({
        'Leido': [leido],
        'Tipo de Cambio': [tipo_cambio],
<<<<<<< HEAD
        'Origen': [origen]})
    # La prioridad proporcionada será la etiqueta de entrenamiento
    y_nueva = [prioridad]  # Prioridad es la etiqueta correspondiente.
    # Entrenamiento incremental del modelo
    modelo_prioridad.partial_fit(X_nueva, y_nueva, classes=[0, 1, 2])
    # Guardar el modelo actualizado
    joblib.dump(modelo_prioridad, MODEL_PATH)

=======
        'Origen': [origen]
    })

    # La prioridad proporcionada será la etiqueta de entrenamiento
    y_nueva = [prioridad]

    # Entrenamiento incremental del modelo
    modelo_prioridad.partial_fit(X_nueva, y_nueva, classes=[0, 1, 2])  # Asegúrate de usar las clases adecuadas para tu caso.

    # Guardar el modelo actualizado
    joblib.dump(modelo_prioridad, MODEL_PATH)
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
