<<<<<<< HEAD
from io import BytesIO
from collections import Counter
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.utils.dateformat import format
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from .models import Notificacion, NotificacionEliminada, NotificacionModificada

from django.shortcuts import render
from .models import Notificacion

def notificacion_list(request):
    """Muestra una lista de notificaciones con opción de filtrado y búsqueda."""
    # Contar las notificaciones no leídas
    unread_notifications_count = Notificacion.objects.filter(leido=False).count()
    prioridad = request.GET.get('prioridad')
    query = request.GET.get('query', '')
    # Filtrar las notificaciones según prioridad y búsqueda
    notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')
    if prioridad:
        notificaciones = notificaciones.filter(prioridad=prioridad)
=======
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
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
    if query:
        notificaciones = notificaciones.filter(mensaje__icontains=query)
    # Pasar las notificaciones y el contador de no leídas a la plantilla
    return render(request, 'notificacion_list.html', {'notificaciones': notificaciones,'query': query,'unread_notifications_count': unread_notifications_count,  # Contador de no leídas
    })

<<<<<<< HEAD

def notificacion_detail(request, pk):
    """Muestra el detalle de una notificación y marca la notificación como leída."""
    notificacion = get_object_or_404(Notificacion, pk=pk)
    notificacion.leido = True
    notificacion.save()
    if notificacion.prioridad is None:
        notificacion.prioridad = clasificar_prioridad(notificacion.leido, notificacion.tipo_cambio, notificacion.origen)
        notificacion.save()
    if 'no ha actualizado su licencia en más de un año' in notificacion.mensaje:
        software_nombre = notificacion.mensaje.split('"')[1]
        software = get_object_or_404(Software, nombre__iexact=software_nombre)
        return render(request, 'notificacion_detail.html', {'notificacion': notificacion, 'software': software})
    return render(request, 'notificacion_detail.html', {'notificacion': notificacion})

def notificacion_delete_selected(request):
    """Elimina las notificaciones seleccionadas y registra cada eliminación en NotificacionEliminada."""
    if request.method == 'POST':
        ids = request.POST.getlist('notificaciones')
        if ids:
            notificaciones_a_eliminar = Notificacion.objects.filter(id__in=ids)
            for notificacion in notificaciones_a_eliminar:
                NotificacionEliminada.objects.create(
                    notificacion=notificacion,
                    fecha_eliminacion=timezone.now()
                )
            notificaciones_a_eliminar.delete()
=======
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
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
            messages.success(request, 'Eliminado correctamente.')
        else:
            messages.error(request, 'No se ha seleccionado ninguna notificación.')
    return redirect('notificacion_list')

def notificacion_change_priority(request):
<<<<<<< HEAD
    """Permite cambiar la prioridad de las notificaciones seleccionadas."""
=======
    # Manejar el cambio de prioridad de notificaciones seleccionadas
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
    if request.method == 'POST':
        ids = request.POST.getlist('notificaciones')
        new_priority = request.POST.get('new_priority')
        if ids and new_priority:
<<<<<<< HEAD
            notificaciones_a_modificar = Notificacion.objects.filter(id__in=ids)
            for notificacion in notificaciones_a_modificar:
                NotificacionModificada.objects.create(
                    notificacion=notificacion,
                    prioridad_anterior=notificacion.prioridad,
                    nueva_prioridad=new_priority,
                    fecha_modificacion=timezone.now())
                notificacion.prioridad = new_priority
                notificacion.save()
            messages.success(request, f'Prioridad cambiada a ({new_priority}) correctamente.')
        else:
            messages.error(request, 'No se ha seleccionado ninguna notificación.')
=======
            Notificacion.objects.filter(id__in=ids).update(prioridad=new_priority)
            messages.success(request, f'Prioridad cambiada a ({new_priority}) correctamente.')
        else:
            messages.error(request, 'No se ha seleccionado ninguna notificación')
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
    return redirect('notificacion_list')

def generar_reporte_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
<<<<<<< HEAD
    elements.append(Paragraph("Reporte de Notificaciones", styles['Title']))
    notifications = Notificacion.objects.all().order_by('-fecha_creacion')
    data_current = [['Mensaje', 'Fecha de Creación', 'Origen', 'Prioridad']]
    for notificacion in notifications:
        fecha_formateada = format(notificacion.fecha_creacion, 'd/m/Y')
        data_current.append([notificacion.mensaje, fecha_formateada, notificacion.origen, notificacion.prioridad])
    table_current = Table(data_current)
    table_current.setStyle(TableStyle([
=======

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
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
<<<<<<< HEAD
        ('GRID', (0,0), (-1,-1), 1, colors.black),]))
    elements.append(Paragraph("Notificaciones Actuales:", styles['Heading2']))
    elements.append(table_current)
    modified_notifications = NotificacionModificada.objects.all().order_by('-fecha_modificacion')
    data_modified = [['Mensaje', 'Prioridad Anterior', 'Nueva Prioridad', 'Fecha de Modificación']]
    for notificacion_modificada in modified_notifications:
        notificacion = notificacion_modificada.notificacion
        fecha_formateada = format(notificacion_modificada.fecha_modificacion, 'd/m/Y')
        data_modified.append([notificacion.mensaje, notificacion_modificada.prioridad_anterior, notificacion_modificada.nueva_prioridad, fecha_formateada])
    table_modified = Table(data_modified)
    table_modified.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),]))
    elements.append(Paragraph("Notificaciones con Cambio de Prioridad:", styles['Heading2']))
    elements.append(table_modified)
=======
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(table)
    
    # Calculate statistics
    from collections import Counter

>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
    priorities = [n.prioridad for n in notifications]
    origins = [n.origen for n in notifications]
    priority_counts = Counter(priorities)
    origin_counts = Counter(origins)
    total_notifications = len(notifications)
<<<<<<< HEAD
    def get_percentage(count):
        return (count / total_notifications * 100) if total_notifications > 0 else 0
    elements.append(Paragraph(" ", styles['Normal']))
    elements.append(Paragraph("Estadísticas:", styles['Heading2']))
=======
    
    def get_percentage(count):
        return (count / total_notifications * 100) if total_notifications > 0 else 0

    # Add statistics to the report
    elements.append(Paragraph(" ", styles['Normal']))  # Add some space
    elements.append(Paragraph("Estadísticas:", styles['Heading2']))

    # Priorities statistics
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
    elements.append(Paragraph("Cantidad y porcentaje de notificaciones por prioridad:", styles['Normal']))
    for priority, count in priority_counts.items():
        percentage = get_percentage(count)
        elements.append(Paragraph(f"Prioridad {priority}: {count} ({percentage:.2f}%)", styles['Normal']))
<<<<<<< HEAD
=======

    # Origins statistics
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
    elements.append(Paragraph("Cantidad y porcentaje de notificaciones por origen:", styles['Normal']))
    for origin, count in origin_counts.items():
        percentage = get_percentage(count)
        elements.append(Paragraph(f"Origen {origin}: {count} ({percentage:.2f}%)", styles['Normal']))
<<<<<<< HEAD
    try:
        plt.figure(figsize=(6, 4))
        plt.pie(priority_counts.values(), labels=priority_counts.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Distribución de Notificaciones por Prioridad')
        priority_chart = BytesIO()
        plt.savefig(priority_chart, format='png')
        priority_chart.seek(0)
        elements.append(Image(priority_chart, width=400, height=200))
        plt.close()
        plt.figure(figsize=(6, 4))
        plt.pie(origin_counts.values(), labels=origin_counts.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Distribución de Notificaciones por Origen')
        origin_chart = BytesIO()
        plt.savefig(origin_chart, format='png')
        origin_chart.seek(0)
        elements.append(Image(origin_chart, width=400, height=200))
        plt.close()
    except Exception as e:
        elements.append(Paragraph(f"Error generando gráficos: {str(e)}", styles['Normal']))
    doc.build(elements)
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reporte.pdf"'
    return response

def notificacion_create(request):
    """Crea una nueva notificación en el sistema y clasifica su prioridad."""
=======

    doc.build(elements)

    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_notificaciones.pdf"'

    return response

def notificacion_create(request):
    # Crear una nueva notificación
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
    if request.method == 'POST':
        mensaje = request.POST['mensaje']
        tipo_cambio = request.POST['tipo_cambio']
        origen = request.POST['origen']
<<<<<<< HEAD
        prioridad_predicha = clasificar_prioridad(False, tipo_cambio, origen)
        Notificacion.objects.create(
=======

        # Clasificar la prioridad usando el modelo entrenado
        prioridad_predicha = clasificar_prioridad(False, tipo_cambio, origen)

        # Crear y guardar la nueva notificación
        nueva_notificacion = Notificacion.objects.create(
>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
            mensaje=mensaje,
            tipo_cambio=tipo_cambio,
            origen=origen,
            prioridad=prioridad_predicha,
<<<<<<< HEAD
            leido=False)
        messages.success(request, 'Notificación creada exitosamente.')
        return redirect('notificacion_list')
=======
            leido=False
        )

        # Entrenar el modelo con la nueva notificación
        entrenar_con_nueva_notificacion(False, tipo_cambio, origen, prioridad_predicha)

        messages.success(request, 'Notificación creada y modelo actualizado correctamente.')
        return redirect('notificacion_list')

>>>>>>> f293c898ee5da6910943c0b56482d0e1395b43d4
    return render(request, 'notificacion_create.html')
