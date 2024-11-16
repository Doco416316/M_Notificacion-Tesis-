# Importa las funciones necesarias desde Django
from django.shortcuts import render, get_object_or_404, redirect
# Importa el modelo Hardware desde el archivo models.py de la misma aplicación
from .models import Hardware
# Importa el formulario HardwareForm desde el archivo forms.py de la misma aplicación
from .forms import HardwareForm
# Importa el modelo Notificacion desde la aplicación de notificaciones
from notifications.models import Notificacion

# Vista para mostrar la lista de todos los hardware
def hardware_list(request):
    hardwares = Hardware.objects.all()  # Obtiene todos los registros del modelo Hardware
    # Renderiza la plantilla 'hardware_list.html' y le pasa los hardware obtenidos
    return render(request, 'hardware_list.html', {'hardwares': hardwares})

# Vista para mostrar los detalles de un hardware específico identificado por su clave primaria (pk)
def hardware_detail(request, pk):
    hardware = get_object_or_404(Hardware, pk=pk)  # Obtiene el hardware o retorna un 404 si no existe
    # Renderiza la plantilla 'hardware_detail.html' y le pasa el hardware obtenido
    return render(request, 'hardware_detail.html', {'hardware': hardware})

# Vista para crear un nuevo hardware
def hardware_create(request):
    if request.method == "POST":  # Verifica si la solicitud es POST (es decir, si el formulario ha sido enviado)
        form = HardwareForm(request.POST)  # Crea un formulario con los datos enviados
        if form.is_valid():  # Valida el formulario
            hardware = form.save()  # Guarda el nuevo hardware en la base de datos
            # Crea una notificación indicando que se ha agregado un nuevo hardware
            Notificacion.objects.create(
                mensaje=f"{hardware.nombre}",
                origen="hardware"
            )
            print("Nombre del hardware ", hardware.nombre)
            # Redirige a la vista de detalles del hardware recién creado
            return redirect('hardware_detail', pk=hardware.pk)
    else:
        form = HardwareForm()  # Si no es una solicitud POST, crea un formulario vacío
    # Renderiza la plantilla 'hardware_form.html' y le pasa el formulario
    return render(request, 'hardware_form.html', {'form': form})

# Vista para actualizar un hardware existente
def hardware_update(request, pk):
    hardware = get_object_or_404(Hardware, pk=pk)  # Obtiene el hardware o retorna un 404 si no existe
    if request.method == "POST":  # Verifica si la solicitud es POST (es decir, si el formulario ha sido enviado)
        form = HardwareForm(request.POST, instance=hardware)  # Crea un formulario con los datos enviados y el hardware existente
        if form.is_valid():  # Valida el formulario
            hardware = form.save()  # Guarda los cambios en la base de datos
            # Crea una notificación indicando que el hardware ha sido modificado
            Notificacion.objects.create(
                mensaje=f"{hardware.nombre}",
                tipo_cambio="modificar",
                origen="hardware"
            )
            # Redirige a la vista de detalles del hardware actualizado
            return redirect('hardware_detail', pk=hardware.pk)
    else:
        form = HardwareForm(instance=hardware)  # Crea un formulario pre-rellenado con el hardware existente
    # Renderiza la plantilla 'hardware_form.html' y le pasa el formulario
    return render(request, 'hardware_form.html', {'form': form})

# Vista para eliminar un hardware existente
def hardware_delete(request, pk):
    hardware = get_object_or_404(Hardware, pk=pk)  # Obtiene el hardware o retorna un 404 si no existe
    if request.method == "POST":  # Verifica si la solicitud es POST (es decir, si el usuario ha confirmado la eliminación)
        hardware.delete()  # Elimina el hardware de la base de datos
        # Crea una notificación indicando que el hardware ha sido eliminado
        Notificacion.objects.create(
            mensaje=f"{hardware.nombre}",
            tipo_cambio="eliminar",
            origen="hardware"
        )
        # Redirige a la vista de lista de hardware
        return redirect('hardware_list')
    # Renderiza la plantilla 'hardware_confirm_delete.html' para confirmar la eliminación
    return render(request, 'hardware_confirm_delete.html', {'hardware': hardware})
