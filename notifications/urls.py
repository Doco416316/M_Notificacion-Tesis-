from django.urls import path
from . import views

urlpatterns = [
    path('', views.notificacion_list, name='notificacion_list'),
    path('detalle/<int:pk>/', views.notificacion_detail, name='notificacion_detail'),
    path('eliminar/', views.notificacion_delete_selected, name='notificacion_delete_selected'),
    path('cambiar-prioridad/', views.notificacion_change_priority, name='notificacion_change_priority'),
    path('reporte/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
]