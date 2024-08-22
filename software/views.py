# Importa las funciones necesarias desde django.shortcuts
from django.shortcuts import render, get_object_or_404, redirect
# Importa el modelo Software desde el módulo actual
from .models import Software
# Importa el formulario SoftwareForm desde el módulo actual
from .forms import SoftwareForm
# Importa el modelo Notificacion desde el módulo de notificaciones
from notifications.models import Notificacion

def software_list(request):
    # Obtiene todos los objetos de Software
    softwares = Software.objects.all()
    # Renderiza la plantilla 'software_list.html' con el contexto de los software
    return render(request, 'software_list.html', {'softwares': softwares})

def software_detail(request, pk):
    # Obtiene el objeto Software específico usando el pk proporcionado
    software = get_object_or_404(Software, pk=pk)
    # Renderiza la plantilla 'software_detail.html' con el contexto del software
    return render(request, 'software_detail.html', {'software': software})

def software_create(request):
    if request.method == "POST":
        # Crea una instancia de SoftwareForm con los datos del POST
        form = SoftwareForm(request.POST)
        if form.is_valid():
            # Guarda el nuevo objeto Software y crea una notificación
            software = form.save()
            notificacion = Notificacion.objects.create(
                mensaje=f"Software {software.nombre} creado"
            )
            print("Nombre del software ", software.nombre)
            # Redirige a la vista de detalles del software creado
            return redirect('software_detail', pk=software.pk)
    else:
        # Si no es un POST, crea un formulario vacío
        form = SoftwareForm()
    # Renderiza la plantilla 'software_form.html' con el contexto del formulario
    return render(request, 'software_form.html', {'form': form})

def software_update(request, pk):
    # Obtiene el objeto Software específico usando el pk proporcionado
    software = get_object_or_404(Software, pk=pk)
    if request.method == "POST":
        # Crea una instancia de SoftwareForm con los datos del POST y el objeto actual
        form = SoftwareForm(request.POST, instance=software)
        if form.is_valid():
            # Guarda los cambios y crea una notificación
            software = form.save()
            notificacion = Notificacion.objects.create(
                mensaje=f"Software {software.nombre} modificado",
                tipo_cambio="modificar"
            )
            # Redirige a la vista de detalles del software actualizado
            return redirect('software_detail', pk=software.pk)
    else:
        # Si no es un POST, crea un formulario con los datos del objeto actual
        form = SoftwareForm(instance=software)
    # Renderiza la plantilla 'software_form.html' con el contexto del formulario
    return render(request, 'software_form.html', {'form': form})

def software_delete(request, pk):
    # Obtiene el objeto Software específico usando el pk proporcionado
    software = get_object_or_404(Software, pk=pk)
    if request.method == "POST":
        # Elimina el objeto Software y crea una notificación
        software.delete()
        notificacion = Notificacion.objects.create(
            mensaje=f"Software {software.nombre} eliminado",
            tipo_cambio="eliminar"
        )
        # Redirige a la lista de software
        return redirect('software_list')
    # Renderiza la plantilla 'software_confirm_delete.html' con el contexto del software
    return render(request, 'software_confirm_delete.html', {'software': software})
