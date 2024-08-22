from django.shortcuts import render, get_object_or_404, redirect  # Importa funciones para manejar vistas, obtener objetos o redirigir URLs.
from django.contrib import messages  # Importa el módulo messages para enviar mensajes de retroalimentación al usuario.
from .models import Notificacion  # Importa el modelo Notificacion.
from django.http import HttpResponse  # Importa HttpResponse para enviar respuestas HTTP personalizadas.
from reportlab.lib.pagesizes import letter  # Importa el tamaño de página carta para PDF.
from reportlab.pdfgen import canvas  # Importa canvas para generar contenido PDF.
from io import BytesIO  # Importa BytesIO para manejar flujos de datos en memoria.
from django.utils.dateformat import format  # Importa la función format para formatear fechas.

def notificacion_list(request):
    # Obtiene el parámetro 'prioridad' de la URL (si existe).
    prioridad = request.GET.get('prioridad')

    # Si se especificó una prioridad, filtra las notificaciones por esa prioridad.
    # Ordena las notificaciones por fecha de creación en orden descendente y limita el resultado a las 10 más recientes.
    if prioridad:
        notificaciones = Notificacion.objects.filter(prioridad=prioridad).order_by('-fecha_creacion')[:10]
    else:
        # Si no se especificó una prioridad, obtiene todas las notificaciones, ordenadas por fecha.
        notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')[:10]
    
    # Renderiza la plantilla 'notificacion_list.html', pasando las notificaciones como contexto.
    return render(request, 'notificacion_list.html', {'notificaciones': notificaciones})

def notificacion_detail(request, pk):
    # Obtiene una notificación específica por su clave primaria (pk) o devuelve un error 404 si no existe.
    notificacion = get_object_or_404(Notificacion, pk=pk)
    
    # Marca la notificación como leída.
    notificacion.leido = True
    notificacion.save()  # Guarda los cambios en la base de datos.
    
    # Renderiza la plantilla 'notificacion_detail.html', pasando la notificación como contexto.
    return render(request, 'notificacion_detail.html', {'notificacion': notificacion})

def notificacion_delete_selected(request):
    # Este método maneja la eliminación de notificaciones seleccionadas por el usuario.

    if request.method == 'POST':
        # Obtiene una lista de IDs de notificaciones seleccionadas del formulario POST.
        ids = request.POST.getlist('notificaciones')
        
        if ids:
            # Si hay IDs seleccionados, elimina las notificaciones correspondientes.
            Notificacion.objects.filter(id__in=ids).delete()
            messages.success(request, 'Notificaciones eliminadas correctamente.')  # Envía un mensaje de éxito al usuario.
        else:
            # Si no se seleccionaron IDs, envía un mensaje de error al usuario.
            messages.error(request, 'No se seleccionaron notificaciones para eliminar.')
    
    # Redirige de vuelta a la lista de notificaciones.
    return redirect('notificacion_list')

def notificacion_change_priority(request):
    # Este método maneja el cambio de prioridad de notificaciones seleccionadas.

    if request.method == 'POST':
        # Obtiene una lista de IDs de notificaciones seleccionadas del formulario POST.
        ids = request.POST.getlist('notificaciones')
        # Obtiene la nueva prioridad seleccionada en el formulario POST.
        new_priority = request.POST.get('new_priority')

        if ids and new_priority:
            # Si hay IDs seleccionados y una nueva prioridad especificada, actualiza la prioridad de esas notificaciones.
            Notificacion.objects.filter(id__in=ids).update(prioridad=new_priority)
            messages.success(request, 'Prioridad de notificaciones cambiada correctamente.')  # Envía un mensaje de éxito al usuario.
        else:
            # Si no se seleccionaron IDs o no se especificó una nueva prioridad, envía un mensaje de error.
            messages.error(request, 'No se seleccionaron notificaciones o no se especificó una nueva prioridad.')
    
    # Redirige de vuelta a la lista de notificaciones.
    return redirect('notificacion_list')

def generar_reporte_pdf(request):
    # Este método genera un reporte en formato PDF con todas las notificaciones.

    # Crea un buffer en memoria para almacenar el PDF temporalmente.
    buffer = BytesIO()
    
    # Crea un objeto canvas para el PDF, usando el buffer como destino.
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # Obtiene las dimensiones de la página carta.
    
    # Escribe los títulos de las columnas en el PDF.
    p.drawString(30, height - 50, "Mensaje")
    p.drawString(250, height - 50, "Fecha de Creación")
    p.drawString(400, height - 50, "Origen")
    
    # Obtiene todas las notificaciones, ordenadas por fecha de creación en orden descendente.
    notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')
    
    # Posición inicial para escribir las filas de notificaciones.
    y_position = height - 70
    
    for notificacion in notificaciones:
        # Formatea la fecha de creación en el formato 'día/mes/año horas:minutos'.
        fecha_formateada = format(notificacion.fecha_creacion, 'd/m/Y H:i')
        
        # Escribe los detalles de la notificación en el PDF.
        p.drawString(30, y_position, notificacion.mensaje)
        p.drawString(250, y_position, fecha_formateada)
        p.drawString(400, y_position, notificacion.origen)
        y_position -= 20  # Desciende la posición vertical para la siguiente notificación.
    
    # Finaliza la página del PDF.
    p.showPage()
    p.save()
    
    # Obtiene el contenido del buffer.
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    
    # Crea una respuesta HTTP con el contenido del PDF, estableciendo el tipo de contenido a 'application/pdf'.
    response = HttpResponse(pdf, content_type='application/pdf')
    # Establece las cabeceras para que el PDF se descargue con un nombre específico.
    response['Content-Disposition'] = 'attachment; filename="reporte_notificaciones.pdf"'
    
    return response  # Devuelve la respuesta con el PDF.
