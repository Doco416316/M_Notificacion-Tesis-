# software/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.software_list, name='software_list'),
    path('<int:pk>/', views.software_detail, name='software_detail'),
    path('nuevo/', views.software_create, name='software_create'),
    path('<int:pk>/editar/', views.software_update, name='software_update'),
    path('<int:pk>/eliminar/', views.software_delete, name='software_delete'),
]
