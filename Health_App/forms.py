from django import forms
from .models import Patient
from .models import Rendezvous
from django.forms import DateTimeInput

class RendezVousForm(forms.ModelForm):
     class Meta:
        model = Rendezvous
        fields = ['date_time', 'patient']
        widgets = {
            'date_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.all()