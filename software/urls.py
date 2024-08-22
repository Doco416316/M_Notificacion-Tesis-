# Importa el módulo path desde django.urls para definir las URL
from django.urls import path
# Importa las vistas desde el módulo actual
from . import views

# Define las URL para la aplicación de software
urlpatterns = [
    # URL para la lista de software, vista asociada: software_list
    path('', views.software_list, name='software_list'),
    
    # URL para los detalles de un software específico, vista asociada: software_detail
    path('<int:pk>/', views.software_detail, name='software_detail'),
    
    # URL para crear un nuevo software, vista asociada: software_create
    path('nuevo/', views.software_create, name='software_create'),
    
    # URL para editar un software específico, vista asociada: software_update
    path('<int:pk>/editar/', views.software_update, name='software_update'),
    
    # URL para eliminar un software específico, vista asociada: software_delete
    path('<int:pk>/eliminar/', views.software_delete, name='software_delete'),
]
