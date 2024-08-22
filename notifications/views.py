from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Notificacion
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.utils.dateformat import format

def notificacion_list(request):
    prioridad = request.GET.get('prioridad')  # Obtener el valor de 'prioridad' de los parámetros GET
    if prioridad:
        notificaciones = Notificacion.objects.filter(prioridad=prioridad).order_by('-fecha_creacion')[:10]
    else:
        notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')[:10]
    return render(request, 'notificacion_list.html', {'notificaciones': notificaciones})

def notificacion_detail(request, pk):
    notificacion = get_object_or_404(Notificacion, pk=pk)
    notificacion.leido = True
    notificacion.save()
    return render(request, 'notificacion_detail.html', {'notificacion': notificacion})

def notificacion_delete_selected(request):
    if request.method == 'POST':
        ids = request.POST.getlist('notificaciones')  # Obtener una lista de IDs seleccionados
        if ids:
            Notificacion.objects.filter(id__in=ids).delete()  # Eliminar las notificaciones seleccionadas
            messages.success(request, 'Notificaciones eliminadas correctamente.')
        else:
            messages.error(request, 'No se seleccionaron notificaciones para eliminar.')
    return redirect('notificacion_list')  # Redirigir de vuelta a la lista de notificaciones

def notificacion_change_priority(request):
    if request.method == 'POST':
        ids = request.POST.getlist('notificaciones')  # Obtener la lista de IDs seleccionados
        new_priority = request.POST.get('new_priority')  # Obtener la nueva prioridad seleccionada

        if ids and new_priority:
            Notificacion.objects.filter(id__in=ids).update(prioridad=new_priority)  # Actualizar la prioridad de las notificaciones seleccionadas
            messages.success(request, 'Prioridad de notificaciones cambiada correctamente.')
        else:
            messages.error(request, 'No se seleccionaron notificaciones o no se especificó una nueva prioridad.')
    
    return redirect('notificacion_list')  # Redirigir de vuelta a la lista de notificaciones

def generar_reporte_pdf(request):
    # Crear un buffer para el PDF
    buffer = BytesIO()
    
    # Crear un objeto PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Títulos de las columnas
    p.drawString(30, height - 50, "Mensaje")
    p.drawString(250, height - 50, "Fecha de Creación")
    p.drawString(400, height - 50, "Origen")
    
    # Obtener todas las notificaciones ordenadas por fecha de creación en orden descendente
    notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')
    
    y_position = height - 70
    
    for notificacion in notificaciones:
        # Formatear la fecha de creación
        fecha_formateada = format(notificacion.fecha_creacion, 'd/m/Y H:i')
        
        p.drawString(30, y_position, notificacion.mensaje)
        p.drawString(250, y_position, fecha_formateada)
        p.drawString(400, y_position, notificacion.origen)
        y_position -= 20
    
    # Finalizar el PDF
    p.showPage()
    p.save()
    
    # Obtener el contenido del buffer
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    
    # Crear una respuesta HTTP con el contenido del PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_notificaciones.pdf"'
    
    return response
