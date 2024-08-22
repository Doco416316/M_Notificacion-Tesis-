# hardware/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Hardware
from .forms import HardwareForm
from notifications.models import Notificacion

def hardware_list(request):
    hardwares = Hardware.objects.all()
    return render(request, 'hardware_list.html', {'hardwares': hardwares})

def hardware_detail(request, pk):
    hardware = get_object_or_404(Hardware, pk=pk)
    return render(request, 'hardware_detail.html', {'hardware': hardware})

def hardware_create(request):
    if request.method == "POST":
        form = HardwareForm(request.POST)
        if form.is_valid():
            hardware = form.save()
            notificacion=Notificacion.objects.create(mensaje=f"Hardware {hardware.nombre} agregado",origen=f"hardware")
            print("Nombre del software ",hardware.nombre)
            return redirect('hardware_detail', pk=hardware.pk)
    else:
        form = HardwareForm()
    return render(request, 'hardware_form.html', {'form': form})

def hardware_update(request, pk):
    hardware = get_object_or_404(Hardware, pk=pk)
    if request.method == "POST":
        form = HardwareForm(request.POST, instance=hardware)
        if form.is_valid():
            hardware = form.save()
            notificacion=Notificacion.objects.create(mensaje=f"Hardware {hardware.nombre} modificado",tipo_cambio=f"modificar",origen=f"hardware")
            return redirect('hardware_detail', pk=hardware.pk)
    else:
        form = HardwareForm(instance=hardware)
    return render(request, 'hardware_form.html', {'form': form})

def hardware_delete(request, pk):
    hardware = get_object_or_404(Hardware, pk=pk)
    if request.method == "POST":
        hardware.delete()
        notificacion=Notificacion.objects.create(mensaje=f"Hardware {hardware.nombre} eliminado",tipo_cambio=f"eliminar",origen=f"hardware")
        return redirect('hardware_list')
    return render(request, 'hardware_confirm_delete.html', {'hardware': hardware})
