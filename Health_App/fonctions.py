from django.utils.timezone import now
from django.db.models import Sum
from django.shortcuts import render
from .models import *
import requests
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import base64
from django.http import JsonResponse
from io import BytesIO
from datetime import datetime, timedelta
from django.db.models import Count, Sum
import io


def statistiques_dans_dashboard(request):
    today = now().date()
    month_start = today.replace(day=1)

    # Nombre de rendez-vous aujourd'hui
    rendez_vous_today_count = Rendezvous.objects.filter(date_time__date=today).count()

    # Total revenu aujourd'hui
    revenu_today = Consultation.objects.filter(rendez_vous__date_time__date=today).aggregate(Sum('montant'))['montant__sum'] or 0

    # Total revenu ce mois
    revenu_month = Consultation.objects.filter(rendez_vous__date_time__date__gte=month_start).aggregate(Sum('montant'))['montant__sum'] or 0

    context = {
        "rendez_vous_today_count": rendez_vous_today_count,
        "revenu_today": revenu_today,
        "revenu_month": revenu_month,
    }

    return context


def generate_plots(request):
    # Define last 6 months dynamically
    today = datetime.today()
    months = [(today - timedelta(days=i*30)).strftime("%Y-%m") for i in range(5, -1, -1)]

    # Initialize data storage
    rendezvous_counts = {month: 0 for month in months}
    montant_totals = {month: 0 for month in months}

    # Query Data
    rendezvous_data = Rendezvous.objects.filter(date_time__gte=today - timedelta(days=180)) \
        .values_list('date_time', flat=True)
    consultation_data = Consultation.objects.filter(rendez_vous__date_time__gte=today - timedelta(days=180)) \
        .values_list('rendez_vous__date_time', 'montant')

    # Process Data
    for rdv_date in rendezvous_data:
        month = rdv_date.strftime("%Y-%m")
        if month in rendezvous_counts:
            rendezvous_counts[month] += 1

    for rdv_date, montant in consultation_data:
        month = rdv_date.strftime("%Y-%m")
        if month in montant_totals:
            montant_totals[month] += montant

    # Prepare data for JSON response
    data = {
        "months": months,
        "rendezvous_counts": list(rendezvous_counts.values()),
        "montant_totals": list(montant_totals.values()),
    }

    return JsonResponse(data)

def save_plot_to_base64(fig):
    """ Convert a Matplotlib figure to base64 image. """
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    return f"data:image/png;base64,{image_base64}"

def plot_rdv_status_distribution(request):
    statuses = Rendezvous.objects.values('status').annotate(count=Count('status'))
    status_labels = [status['status'] for status in statuses]
    status_counts = [status['count'] for status in statuses]

    data = {
        "labels": status_labels,
        "data": status_counts,
    }

    return JsonResponse(data)

def plot_montant_by_patient(request):
    # Calculer la date il y a 6 mois
    six_months_ago = datetime.now() - timedelta(days=180)

    # Récupérer les données des patients avec le montant total dépensé dans les 6 derniers mois
    data = Consultation.objects.filter(
        rendez_vous__date_time__gte=six_months_ago  # Filtrer les consultations des 6 derniers mois
    ).values('patient__nom').annotate(
        total_montant=Sum('montant')  # Montant total dépensé par patient
    ).order_by('-total_montant')[:3]  # Trier par montant total décroissant et prendre les 3 premiers

    # Extraire les labels (noms des patients) et les valeurs (montant total)
    labels = [entry['patient__nom'] for entry in data]
    total_montants = [round(entry['total_montant'], 2) if entry['total_montant'] is not None else 0.00 for entry in data]

    # Préparer les données pour la réponse JSON
    response_data = {
        "labels": labels,
        "total_montants": total_montants,
    }
    print(response_data)

    return JsonResponse(response_data)

 

def plot_consultation_validation_status(request):
    validated = Consultation.objects.filter(is_validate=True).count()
    non_validated = Consultation.objects.filter(is_validate=False).count()

    data = {
        "labels": ["Validé", "Non Validé"],
        "data": [validated, non_validated],
    }

    return JsonResponse(data)

