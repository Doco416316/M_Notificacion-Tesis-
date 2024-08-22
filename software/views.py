# software/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Software
from .forms import SoftwareForm
from notifications.models import Notificacion

def software_list(request):
    softwares = Software.objects.all()
    return render(request, 'software_list.html', {'softwares': softwares})

def software_detail(request, pk):
    software = get_object_or_404(Software, pk=pk)
    return render(request, 'software_detail.html', {'software': software})

def software_create(request):
    if request.method == "POST":
        form = SoftwareForm(request.POST)
        if form.is_valid():
            software = form.save()
            notificacion=Notificacion.objects.create(mensaje=f"Software {software.nombre} creado")
            print("Nombre del software ",software.nombre)
            return redirect('software_detail', pk=software.pk)
    else:
        form = SoftwareForm()
    return render(request, 'software_form.html', {'form': form})

def software_update(request, pk):
    software = get_object_or_404(Software, pk=pk)
    if request.method == "POST":
        form = SoftwareForm(request.POST, instance=software)
        if form.is_valid():
            software = form.save()
            notificacion=Notificacion.objects.create(mensaje=f"Software {software.nombre} modificado",tipo_cambio=f"modificar")
            return redirect('software_detail', pk=software.pk)
    else:
        form = SoftwareForm(instance=software)
    return render(request, 'software_form.html', {'form': form})

def software_delete(request, pk):
    software = get_object_or_404(Software, pk=pk)
    if request.method == "POST":
        software.delete()
        notificacion=Notificacion.objects.create(mensaje=f"Software {software.nombre} eliminado",tipo_cambio=f"eliminar")
        return redirect('software_list')
    return render(request, 'software_confirm_delete.html', {'software': software})
