# Importa la función path de Django para definir las rutas (URLs) de la aplicación
from django.urls import path
# Importa las vistas desde el archivo views.py de la misma aplicación
from . import views

# Define la lista de patrones de URL para la aplicación hardware
urlpatterns = [
    # Ruta para la lista de hardware. Se ejecuta la vista 'hardware_list' cuando la URL raíz es accedida
    path('', views.hardware_list, name='hardware_list'),

    # Ruta para ver los detalles de un hardware específico, identificado por su clave primaria (pk)
    path('<int:pk>/', views.hardware_detail, name='hardware_detail'),

    # Ruta para crear un nuevo hardware. Se ejecuta la vista 'hardware_create'
    path('nuevo/', views.hardware_create, name='hardware_create'),

    # Ruta para editar un hardware existente, identificado por su clave primaria (pk)
    path('<int:pk>/editar/', views.hardware_update, name='hardware_update'),

    # Ruta para eliminar un hardware existente, identificado por su clave primaria (pk)
    path('<int:pk>/eliminar/', views.hardware_delete, name='hardware_delete'),
]
