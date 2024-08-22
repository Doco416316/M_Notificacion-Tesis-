# software/forms.py
from django import forms
from .models import Software

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ['nombre', 'version', 'licencia', 'fecha_instalacion']
