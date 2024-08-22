from django.urls import path  # Importa la función path, utilizada para definir rutas de URL en Django.
from . import views  # Importa el módulo views desde el mismo paquete (aplicación).

# Definición de las rutas de URL para la aplicación de notificaciones
urlpatterns = [
    # Ruta para la vista que muestra la lista de notificaciones.
    # Esta es la ruta principal ('') que apunta a la función 'notificacion_list' en views.
    path('', views.notificacion_list, name='notificacion_list'),

    # Ruta para la vista de detalle de una notificación específica.
    # El '<int:pk>' captura un número entero de la URL que se pasa como argumento 'pk' a la vista 'notificacion_detail'.
    path('detalle/<int:pk>/', views.notificacion_detail, name='notificacion_detail'),

    # Ruta para la vista que permite eliminar notificaciones seleccionadas.
    # Apunta a la función 'notificacion_delete_selected' en views.
    path('eliminar/', views.notificacion_delete_selected, name='notificacion_delete_selected'),

    # Ruta para la vista que permite cambiar la prioridad de las notificaciones seleccionadas.
    # Apunta a la función 'notificacion_change_priority' en views.
    path('cambiar-prioridad/', views.notificacion_change_priority, name='notificacion_change_priority'),

    # Ruta para la vista que genera un reporte en formato PDF de las notificaciones.
    # Apunta a la función 'generar_reporte_pdf' en views.
    path('reporte/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
]
