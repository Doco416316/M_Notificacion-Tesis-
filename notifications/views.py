from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Notificacion
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from django.utils.dateformat import format
from .ml_model import clasificar_prioridad, entrenar_con_nueva_notificacion

def notificacion_list(request):
    # Obtener el parámetro 'prioridad' de la URL (si existe)
    prioridad = request.GET.get('prioridad')

    # Obtener el término de búsqueda del parámetro 'query' de la URL (si existe)
    query = request.GET.get('query', '')

    # Filtrar las notificaciones por prioridad si se especifica
    if prioridad:
        notificaciones = Notificacion.objects.filter(prioridad=prioridad).order_by('-fecha_creacion')
    else:
        # Obtener todas las notificaciones ordenadas por fecha si no se especifica prioridad
        notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')

    # Filtrar por término de búsqueda en el contenido del mensaje
    if query:
        notificaciones = notificaciones.filter(mensaje__icontains=query)

    # Limitar el resultado a las 30 notificaciones más recientes
    notificaciones = notificaciones[:30]

    return render(request, 'notificacion_list.html', {'notificaciones': notificaciones, 'query': query})

def notificacion_detail(request, pk):
    # Obtener una notificación específica o un 404 si no existe
    notificacion = get_object_or_404(Notificacion, pk=pk)

    # Marcar la notificación como leída y guardar
    notificacion.leido = True
    notificacion.save()

    # Si la notificación aún no tiene una prioridad asignada, clasificarla
    if notificacion.prioridad is None:
        notificacion.prioridad = clasificar_prioridad(notificacion.leido, notificacion.tipo_cambio, notificacion.origen)
        notificacion.save()

    return render(request, 'notificacion_detail.html', {'notificacion': notificacion})

def notificacion_delete_selected(request):
    # Manejar la eliminación de notificaciones seleccionadas
    if request.method == 'POST':
        ids = request.POST.getlist('notificaciones')
        if ids:
            Notificacion.objects.filter(id__in=ids).delete()
            messages.success(request, 'Eliminado correctamente.')
        else:
            messages.error(request, 'No se ha seleccionado ninguna notificación.')
    return redirect('notificacion_list')

def notificacion_change_priority(request):
    # Manejar el cambio de prioridad de notificaciones seleccionadas
    if request.method == 'POST':
        ids = request.POST.getlist('notificaciones')
        new_priority = request.POST.get('new_priority')

        if ids and new_priority:
            Notificacion.objects.filter(id__in=ids).update(prioridad=new_priority)
            messages.success(request, f'Prioridad cambiada a ({new_priority}) correctamente.')
        else:
            messages.error(request, 'No se ha seleccionado ninguna notificación')
    return redirect('notificacion_list')

def generar_reporte_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add title
    title = Paragraph("Reporte de Notificaciones", styles['Title'])
    elements.append(title)

    # Prepare data for the table
    notifications = Notificacion.objects.all().order_by('-fecha_creacion')
    data = [['Mensaje', 'Fecha de Creación', 'Origen', 'Prioridad']]
    for notificacion in notifications:
        fecha_formateada = format(notificacion.fecha_creacion, 'd/m/Y H:i')
        data.append([notificacion.mensaje, fecha_formateada, notificacion.origen, notificacion.prioridad])
    
    # Create table with data
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(table)
    
    # Calculate statistics
    from collections import Counter

    priorities = [n.prioridad for n in notifications]
    origins = [n.origen for n in notifications]
    priority_counts = Counter(priorities)
    origin_counts = Counter(origins)
    total_notifications = len(notifications)
    
    def get_percentage(count):
        return (count / total_notifications * 100) if total_notifications > 0 else 0

    # Add statistics to the report
    elements.append(Paragraph(" ", styles['Normal']))  # Add some space
    elements.append(Paragraph("Estadísticas:", styles['Heading2']))

    # Priorities statistics
    elements.append(Paragraph("Cantidad y porcentaje de notificaciones por prioridad:", styles['Normal']))
    for priority, count in priority_counts.items():
        percentage = get_percentage(count)
        elements.append(Paragraph(f"Prioridad {priority}: {count} ({percentage:.2f}%)", styles['Normal']))

    # Origins statistics
    elements.append(Paragraph("Cantidad y porcentaje de notificaciones por origen:", styles['Normal']))
    for origin, count in origin_counts.items():
        percentage = get_percentage(count)
        elements.append(Paragraph(f"Origen {origin}: {count} ({percentage:.2f}%)", styles['Normal']))

    doc.build(elements)

    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_notificaciones.pdf"'

    return response

def notificacion_create(request):
    # Crear una nueva notificación
    if request.method == 'POST':
        mensaje = request.POST['mensaje']
        tipo_cambio = request.POST['tipo_cambio']
        origen = request.POST['origen']

        # Clasificar la prioridad usando el modelo entrenado
        prioridad_predicha = clasificar_prioridad(False, tipo_cambio, origen)

        # Crear y guardar la nueva notificación
        nueva_notificacion = Notificacion.objects.create(
            mensaje=mensaje,
            tipo_cambio=tipo_cambio,
            origen=origen,
            prioridad=prioridad_predicha,
            leido=False
        )

        # Entrenar el modelo con la nueva notificación
        entrenar_con_nueva_notificacion(False, tipo_cambio, origen, prioridad_predicha)

        messages.success(request, 'Notificación creada y modelo actualizado correctamente.')
        return redirect('notificacion_list')

    return render(request, 'notificacion_create.html')
