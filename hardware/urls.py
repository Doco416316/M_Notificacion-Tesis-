# hardware/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hardware_list, name='hardware_list'),
    path('<int:pk>/', views.hardware_detail, name='hardware_detail'),
    path('nuevo/', views.hardware_create, name='hardware_create'),
    path('<int:pk>/editar/', views.hardware_update, name='hardware_update'),
    path('<int:pk>/eliminar/', views.hardware_delete, name='hardware_delete'),
]
