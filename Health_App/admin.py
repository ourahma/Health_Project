from django.contrib import admin
from .models import *

@admin.register(Medcin)
class MedcinAdmin(admin.ModelAdmin):
    list_display = ["email", "nom", "prenom", "specialite", "is_superuser"]
    search_fields = ["email", "nom", "prenom"]


admin.site.register(Maladie)
admin.site.register(Rendezvous)
admin.site.register(Consultation)
admin.site.register(Secretaire)
admin.site.register(Patient)
admin.site.register(PredictionDiabete)
