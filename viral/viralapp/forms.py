from django import forms
from .models import Certificate, Projects

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'

class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'
