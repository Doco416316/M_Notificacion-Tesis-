# Importa las funciones necesarias desde django.shortcuts
from django.shortcuts import render, get_object_or_404, redirect
# Importa el modelo Software desde el módulo actual
from .models import Software
# Importa el formulario SoftwareForm desde el módulo actual
from .forms import SoftwareForm
# Importa el modelo Notificacion desde el módulo de notificaciones
from notifications.models import Notificacion

def software_list(request):
    """
    Vista para listar todos los objetos de Software.
    """
    softwares = Software.objects.all()  # Obtiene todos los objetos de Software
    return render(request, 'software_list.html', {'softwares': softwares})  # Renderiza la plantilla

def software_detail(request, pk):
    """
    Vista para mostrar los detalles de un software específico.
    
    :param pk: Clave primaria del software a mostrar.
    """
    software = get_object_or_404(Software, pk=pk)  # Obtiene el objeto Software específico
    return render(request, 'software_detail.html', {'software': software})  # Renderiza la plantilla

def software_create(request):
    """
    Vista para crear un nuevo software.
    """
    if request.method == "POST":
        form = SoftwareForm(request.POST)  # Crea una instancia del formulario con los datos del POST
        if form.is_valid():
            software = form.save()  # Guarda el nuevo objeto Software
            # Crea una notificación para el software creado
            Notificacion.objects.create(mensaje=f"{software.nombre}")
            return redirect('software_detail', pk=software.pk)  # Redirige a los detalles del software
    else:
        form = SoftwareForm()  # Si no es un POST, crea un formulario vacío
    return render(request, 'software_form.html', {'form': form})  # Renderiza la plantilla

def software_update(request, pk):
    """
    Vista para editar un software existente.
    
    :param pk: Clave primaria del software a editar.
    """
    software = get_object_or_404(Software, pk=pk)  # Obtiene el objeto Software específico
    if request.method == "POST":
        form = SoftwareForm(request.POST, instance=software)  # Crea el formulario con los datos actuales
        if form.is_valid():
            software = form.save()  # Guarda los cambios
            # Crea una notificación para el software modificado
            Notificacion.objects.create(mensaje=f"{software.nombre}", tipo_cambio="modificar")
            return redirect('software_detail', pk=software.pk)  # Redirige a los detalles del software
    else:
        form = SoftwareForm(instance=software)  # Si no es un POST, crea un formulario con los datos actuales
    return render(request, 'software_form.html', {'form': form})  # Renderiza la plantilla

def software_delete(request, pk):
    """
    Vista para eliminar un software existente.
    
    :param pk: Clave primaria del software a eliminar.
    """
    software = get_object_or_404(Software, pk=pk)  # Obtiene el objeto Software específico
    if request.method == "POST":
        software.delete()  # Elimina el objeto Software
        # Crea una notificación para el software eliminado
        Notificacion.objects.create(mensaje=f"{software.nombre}", tipo_cambio="eliminar")
        return redirect('software_list')  # Redirige a la lista de software
    return render(request, 'software_confirm_delete.html', {'software': software})  # Renderiza la plantilla
