from django.urls import path
from . import views
from .views import maladie 

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("test/", views.test, name="test"),
    
    
     
    path('maladie/', views.maladie, name='maladie'),
    path('modifier_maladie/<int:maladie_id>/', views.modifier_maladie, name='modifier_maladie'),
    
    
    ## la prédiction sur le diabetes    
    path("diabetes_prediction/", views.diabetes_prediction, name="diabetes_prediction"),
    
    
    
    
    ### gerer les secretaires pour un medcin 
    path("secretaires/", views.gerersecretaires, name="secretaires"),
    path("supprimer-secretaire/<int:secretaire_id>/", views.supprimer_secretaire, name="supprimer_secretaire"),
    path('modifier_secretaire/<int:secretaire_id>/', views.modifier_secretaire, name='modifier_secretaire'),
     
    ### les visualisations dans dashboard
     
    path('test/', views.test, name='test'),
    path('generate-plots/', views.generate_plots_view, name='generate_plots'),
    path('rdv-status-distribution/', views.rdv_status_distribution_view, name='rdv_status_distribution'),
    path('montant-by-patient/', views.montant_by_patient_view, name='montant_by_patient'),
    path('consultation-validation-status/', views.consultation_validation_status_view, name='consultation_validation_status'),
    path('statistiques-diabete/', views.statistiques_diabete, name='statistiques_diabete'),
    path('evolution_statistiques_diabete/', views.evolution_statistiques_diabete, name='evolution_statistiques_diabete'),
    
    
    
    path('afficher_consultations', views.afficher_consultations, name='afficher_consultations'),
    path('pages/consultation/', views.consultation_view, name='consultation_view'),
    path('ajouter-maladie/<int:consultation_id>/', views.ajouter_maladie, name='ajouter_maladie'),
    path('generer-rapport/<int:consultation_id>/', views.generer_rapport, name='generer_rapport'),
    path('pages/rendez-vous/', views.rendez, name='rendez_vous'),
    path('valider_rendez_vous/<int:rendez_vous_id>/', views.valider_rendez_vous, name='valider_rendez_vous'),
    path('liste_rendez_vous_valides/', views.liste_rendez_vous_valides, name='liste_rendez_vous_valides'),
   
    path('modifier-rendez-vous/<int:rendez_vous_id>/', views.modifier_rendez_vous, name='modifier_rendez_vous'),
    path('supprimer-rendez-vous/<int:rendez_vous_id>/', views.supprimer_rendez_vous, name='supprimer_rendez_vous'),
]