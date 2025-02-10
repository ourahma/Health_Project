from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .decorators import medcin_required
from django.contrib.auth import authenticate, logout, login as auth_login
from .fonctions import *
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import *
from .predictions import *
from django.core.files.storage import default_storage
from .forms import *
from django.utils import timezone



@login_required
@medcin_required
### Return index page
def home(request):
    context=statistiques_dans_dashboard(request)
    return render(request, 'pages/index.html', context)



## créer login view and return home is user is loggedin 

def login_view(request):
 
    if request.user.is_authenticated:
        return redirect("home")  # Redirect if already logged in

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('mdp')
        
        user = authenticate(request, email=email, password=password)
        print("user is ---> ",user)
        if user and (isinstance(user, Medcin) or isinstance(user, Secretaire)):
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Vous n'avez pas accès, vous devez être un Medcin ou un Secretaire")
            return render(request, "pages/login.html")  # Re-render login page with error message

    return render(request, "pages/login.html")

## la méthode de logout
def logout_view(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté avec succès")
    return redirect("login")

## faire la prédiction sur le diabetes 
def diabetes_prediction(request):
    patients = Patient.objects.all()  # Récupérer tous les patients

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        glucose = request.POST.get('glucose')
        insuline = request.POST.get('insuline')
        bmi = request.POST.get('bmi')
        age = request.POST.get('age')

        if not patient_id or not glucose or not insuline or not bmi or not age:
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'pages/diabetes_prediction.html', {'patients': patients})

        try:
            glucose = float(glucose)
            insuline = float(insuline)
            bmi = float(bmi)
            age = int(age)
        except ValueError:
            messages.error(request, "Veuillez entrer des valeurs valides.")
            return render(request, 'pages/diabetes_prediction.html', {'patients': patients})

        # Récupération du patient
        patient = get_object_or_404(Patient, id=patient_id)

        # Prédiction
        prediction, probability_percentage = make_diabetes_prediction(glucose, insuline, bmi, age)

        # Enregistrement dans la base de données
        PredictionDiabete.objects.create(
            patient=patient,
            glucose=glucose,
            insuline=insuline,
            bmi=bmi,
            age=age,
            resultat=prediction
        )

        return render(request, 'pages/diabetes_prediction.html', {
            'patients': patients,
            'prediction': prediction,
            'probability_percentage': probability_percentage,
            'patient': patient
        })

    return render(request, 'pages/diabetes_prediction.html', {'patients': patients})





## gerer les secretaires pour un medcin
User = get_user_model()

@login_required
@medcin_required
def gerersecretaires(request):
    if not request.user.is_medcin():
        messages.error(request, "Seuls les médecins peuvent ajouter des secrétaires.")
        return redirect('home')

    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        password = request.POST.get("mdp")
        phone_number = request.POST.get("phone_number")
        photo = request.FILES.get("img")

        # Vérifier que tous les champs sont remplis
        if not all([nom, prenom, email, password]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return redirect("secretaires")

        # Vérifier si l'email est déjà utilisé
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect("secretaires")

        # Créer un utilisateur Secretaire
        user = User.objects.create_user(email=email, password=password, nom=nom, prenom=prenom)
        user.is_staff = True  # Pour permettre l'accès à l'administration si besoin
        user.save()

        # Associer à un modèle Secretaire
        secretaire = Secretaire.objects.create(
            user=user,
            phone_number=phone_number,
            profile_picture=photo if photo else None,
            medcin=request.user.medcin
        )

        messages.success(request, "Secrétaire ajouté avec succès !")
        return redirect("secretaires")
    
    secretaires = Secretaire.objects.all()
    return render(request, 'pages/manage_secretaires.html', {'secretaires': secretaires})
    
    
@login_required
def supprimer_secretaire(request, secretaire_id):
    print("supprimer is triggered")
    secretaire = get_object_or_404(Secretaire, id=secretaire_id)

    if not request.user.is_medcin():
        messages.error(request, "Seuls les médecins peuvent supprimer un secrétaire.")
        return redirect("home")

    if secretaire.profile_picture:
        default_storage.delete(secretaire.profile_picture.path)  # Supprimer l'image

    secretaire.delete()
    messages.success(request, "Secrétaire supprimé avec succès !")
    return redirect("secretaires")


def modifier_secretaire(request, secretaire_id):
    secretaire = get_object_or_404(Secretaire, id=secretaire_id)

    if request.method == 'POST':
        # Retrieve the data from POST and FILES
        secretaire.nom = request.POST.get('nom', secretaire.nom)
        secretaire.prenom = request.POST.get('prenom', secretaire.prenom)
        secretaire.email = request.POST.get('email', secretaire.email)
        secretaire.phone_number = request.POST.get('phone_number', secretaire.phone_number)
        secretaire.mdp = request.POST.get('mdp', secretaire.mdp)

        # Check if the profile picture has been updated
        if 'profile_picture' in request.FILES:
            secretaire.profile_picture = request.FILES['profile_picture']

        # Save the updated Secretaire object
        secretaire.save()
        messages.success(request, "Secrétaire modifié avec succès !")
        # Redirect after saving
        return redirect('secretaires')  # Modify this to your appropriate redirect target
    
    else:
        # For GET request, simply render the page with the existing Secretaire info
        return render(request, 'pages/modifier_secretaire.html', {'secretaire': secretaire})
    
def test(request):
    context=statistiques_dans_dashboard(request)
    return render(request, 'pages/test.html',context)

def generate_plots_view(request):
    return generate_plots(request)

def rdv_status_distribution_view(request):
    return plot_rdv_status_distribution(request)

def montant_by_patient_view(request):
    return plot_montant_by_patient(request)

def consultation_validation_status_view(request):
    return plot_consultation_validation_status(request)


## la page maladie
def modifier_maladie(request, maladie_id):
    maladie = get_object_or_404(Maladie, id=maladie_id)
    
    if request.method == "POST":
        # Récupérer les valeurs soumises par l'utilisateur
        nom = request.POST.get('nom', maladie.nom).strip()
        description = request.POST.get('description', maladie.description).strip()
        symptoms_str = request.POST.get('symptoms', ", ".join(maladie.get_symptoms_list())).strip()
        traitements_str = request.POST.get('traitements', ", ".join(maladie.traitements)).strip()
        # Nettoyer et convertir les chaînes en listes
        symptoms_list = [s.strip() for s in symptoms_str.split(",") if s.strip()]
        traitements_list = [t.strip() for t in traitements_str.split(",") if t.strip()]
        # Mettre à jour les champs
        maladie.nom = nom
        maladie.description = description
        maladie.set_symptoms_list(symptoms_list)
        maladie.set_traitements_list(traitements_list)
        # Sauvegarder la maladie
        maladie.save()
        # Message de succès
        messages.success(request, "Maladie modifiée avec succès.")
        return redirect('maladie')  # Rediriger après la modification
    
    return redirect('maladie')  # Si ce n'est pas une requête POST, rediriger vers la page des maladies
###################################################################
def maladie(request):
    maladies = Maladie.objects.all()
    print(f"Maladies trouvées: {maladies}")  # Ajoute ceci
    return render(request, 'pages/maladie.html',{'maladies': maladies})
def modifier_maladie(request, maladie_id):
    maladie = get_object_or_404(Maladie, id=maladie_id)
    
    if request.method == "POST":
        # Récupérer les valeurs soumises par l'utilisateur
        nom = request.POST.get('nom', maladie.nom).strip()
        description = request.POST.get('description', maladie.description).strip()
        symptoms_str = request.POST.get('symptoms', ", ".join(maladie.get_symptoms_list())).strip()
        traitements_str = request.POST.get('traitements', ", ".join(maladie.traitements)).strip()

        # Nettoyer et convertir les chaînes en listes
        symptoms_list = [s.strip() for s in symptoms_str.split(",") if s.strip()]
        traitements_list = [t.strip() for t in traitements_str.split(",") if t.strip()]

        # Mettre à jour les champs
        maladie.nom = nom
        maladie.description = description
        maladie.set_symptoms_list(symptoms_list)
        maladie.set_traitements_list(traitements_list)

        # Sauvegarder la maladie
        maladie.save()

        # Message de succès
        messages.success(request, "Maladie modifiée avec succès.")
        return redirect('maladie')  # Rediriger après la modification
    
    return redirect('maladie')  # Si ce n'est pas une requête POST, rediriger vers la page des maladies

###################################################################
@login_required
@medcin_required
def maladie(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'ajouter':
            nom = request.POST.get('nom')
            description = request.POST.get('description')
            symptoms_str = request.POST.get('symptoms')  # Symptômes sous forme de chaîne
            traitements_str = request.POST.get('traitements')  # Traitements sous forme de chaîne

            # Vérification si les champs requis sont remplis
            if not nom or not description:
                messages.error(request, "Le nom et la description sont obligatoires.")
                return redirect('nom_de_votre_vue')  # Remplacez par la vue appropriée

            # Convertir les chaînes en listes
            symptoms_list = symptoms_str.split(",") if symptoms_str else []
            traitements_list = traitements_str.split(",") if traitements_str else []

            # Si les champs sont vides, les mettre à None ou une valeur par défaut
            if not symptoms_list:
                symptoms_list = None
            if not traitements_list:
                traitements_list = None

            # Créer une nouvelle instance de la maladie
            nouvelle_maladie = Maladie.objects.create(
                nom=nom,
                description=description,
                symptoms=",".join(symptoms_list) if symptoms_list else "",
                traitements=",".join(traitements_list) if traitements_list else "",
            )

            # Sauvegarder l'objet
            nouvelle_maladie.save()

            messages.success(request, "Maladie ajoutée avec succès.")
        
        
                # Handle "modifier" (Modify an existing disease)
        elif action == 'modifier':
            maladie_id = request.POST.get('maladie_id')
            maladie = get_object_or_404(Maladie, id=maladie_id)

            # Get values from the form and make sure description is not empty
            nom = request.POST.get('nom')
            description = request.POST.get('description')  # Ensure it's not empty
            if not description:
                description = "Description not provided"  # Default value or handle error

            symptoms_str = request.POST.get('symptoms')  # Symptoms as a string
            traitements_str = request.POST.get('traitements')  # Treatments as a string

            # Convert strings to lists
            symptoms_list = symptoms_str.split(",") if symptoms_str else []
            traitements_list = traitements_str.split(",") if traitements_str else []

            # Update the fields
            maladie.nom = nom
            maladie.description = description
            maladie.set_symptoms_list(symptoms_list)
            maladie.set_traitements_list(traitements_list)

            # Save the updated maladie
            maladie.save()

            messages.success(request, "Maladie modifiée avec succès.")

                    
        # Handle "supprimer" (Delete a disease)
        elif action == 'supprimer':
            maladie_id = request.POST.get('maladie_id')
            maladie = get_object_or_404(Maladie, id=maladie_id)
            maladie.delete()

            messages.success(request, "Maladie supprimée avec succès.")

        # Redirect to the same page after the action
        return redirect('maladie')  # Adjust this if needed to the correct URL

    # Retrieve all diseases for

    maladies = Maladie.objects.all()

    return render(request, 'pages/maladie.html', {'maladies': maladies})

@login_required
@login_required

def rendez(request):
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rendez_vous = form.save()
            messages.success(request, "Rendez-vous créé avec succès.")
            return redirect('rendez_vous')
    else:
        form = RendezVousForm()

    # Récupérer les rendez-vous en attente
    rendez_vous_list = Rendezvous.objects.filter(status='en attente')

    # Vérifier les rendez-vous dont la date est dépassée
    maintenant = timezone.now()
    rendez_vous_delai_depasse = [rv for rv in rendez_vous_list if rv.date_time < maintenant]

    # S'il existe des rendez-vous dont la date est dépassée, ajouter une alerte
    if rendez_vous_delai_depasse:
        messages.error(request, "Il existe des rendez-vous non validés dont la date est dépassée.")

    return render(request, 'pages/rendez-vous.html', {
        'form': form,
        'rendez_vous_list': rendez_vous_list,
        'rendez_vous_delai_depasse': rendez_vous_delai_depasse
        
    })


def valider_rendez_vous(request, rendez_vous_id):
    rendez_vous = get_object_or_404(Rendezvous, id=rendez_vous_id)

    if request.method == "POST":
        montant = request.POST.get("montant")

        if not montant:
            messages.error(request, "Veuillez entrer un montant valide.")
            return redirect("rendez_vous")

        # Convertir en nombre décimal
        try:
            montant = float(montant)
        except ValueError:
            messages.error(request, "Le montant doit être un nombre valide.")
            return redirect("rendez_vous")

        # Valider le rendez-vous
        rendez_vous.status = "validé"
        rendez_vous.save()

        # Vérifier si une consultation existe déjà pour ce rendez-vous
        consultation, created = Consultation.objects.get_or_create(
            rendez_vous=rendez_vous,
            defaults={"is_validate": True, "patient": rendez_vous.patient, "montant": montant}
        )

        # Si la consultation existe déjà, on met à jour son montant
        if not created:
            consultation.montant = montant
            consultation.save()

        messages.success(request, "Rendez-vous validé et consultation enregistrée.")
        return redirect("rendez_vous")

    # Passer la liste des rendez-vous avec leurs consultations
    rendez_vous_list = Rendezvous.objects.all().prefetch_related("consultation")

    return render(request, "rendez_vous.html", {"rendez_vous_list": rendez_vous_list})
def liste_rendez_vous_valides(request):
    # Récupérer les rendez-vous validés
    rendez_vous_valides = Rendezvous.objects.filter(status='validé').select_related('patient', 'consultation')

    return render(request, 'pages/liste_rendez_vous_valides.html', {
        'rendez_vous_valides': rendez_vous_valides
    })


@login_required
def supprimer_rendez_vous(request, rendez_vous_id):
    rendez_vous = get_object_or_404(Rendezvous, id=rendez_vous_id)

    rendez_vous.delete()
    messages.success(request, "Rendez-vous supprimé avec succès.")
    return redirect("rendez_vous")

@login_required
def modifier_rendez_vous(request, rendez_vous_id):
    rendez_vous = get_object_or_404(Rendezvous, id=rendez_vous_id)
    
    if request.method == "POST":
        form = RendezVousForm(request.POST, instance=rendez_vous)
        if form.is_valid():
            form.save()
            messages.success(request, "Rendez-vous modifié avec succès.")
            return redirect("rendez_vous")
    else:
        form = RendezVousForm(instance=rendez_vous)
    
    return render(request, 'pages/modifier_rendez_vous.html', {'form': form, 'rendez_vous': rendez_vous})










def consultation_view(request):
    consultations = Consultation.objects.all().select_related('rendez_vous', 'maladie')
    maladies = Maladie.objects.all()
    return render(request, 'pages/consultation.html', {'consultations': consultations, 'maladies': maladies})

def ajouter_maladie(request, consultation_id):
    if request.method == "POST":
        consultation = get_object_or_404(Consultation, id=consultation_id)
        maladie_id = request.POST.get('maladie')
        maladie = get_object_or_404(Maladie, id=maladie_id)
        consultation.maladie = maladie
        consultation.save()
        messages.success(request, "Maladie ajoutée avec succès.")
    return redirect('consultation_view')




from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def generer_rapport(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="rapport_{consultation.rendez_vous.patient.nom}_{consultation.rendez_vous.patient.prenom}.pdf"'

    p = canvas.Canvas(response)
    width, height = p._pagesize

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, 800, "Rapport de consultation")
    p.setFont("Helvetica", 12)
    
    # Ajout d'un espace entre le titre et les informations
    y_position = 750
    
    p.drawString(100, y_position, f"Nom: {consultation.rendez_vous.patient.nom}")
    p.drawString(100, y_position - 20, f"Prénom: {consultation.rendez_vous.patient.prenom}")
    p.drawString(100, y_position - 40, f"CNI: {consultation.rendez_vous.patient.cni}")
    p.drawString(100, y_position - 60, f"Date du rendez-vous: {consultation.rendez_vous.date_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if consultation.maladie:
        p.drawString(100, y_position - 80, f"Maladie: {consultation.maladie.nom}")
        p.drawString(100, y_position - 100, f"Symptômes: {consultation.maladie.symptoms}")
        p.drawString(100, y_position - 120, f"Traitements: {consultation.maladie.traitements}")
    else:
        p.drawString(100, y_position - 80, "Maladie: Non spécifiée")

    p.showPage()
    p.save()
    return response

    return response


def afficher_consultations(request):
    consultations = Consultation.objects.all()
    return render(request, 'pages/afficher_consultations.html', {'consultations': consultations})



def statistiques_diabete(request):
    total_predictions = PredictionDiabete.objects.count()
    diabetique = PredictionDiabete.objects.filter(resultat=True).count()
    non_diabetique = total_predictions - diabetique

    data = {
        "labels": ["Diabétique", "Non Diabétique"],
        "data": [diabetique, non_diabetique],
    }
    return JsonResponse(data)



def evolution_statistiques_diabete(request):
   
    today = now()
    months = [(today - timedelta(days=30 * i)).strftime('%Y-%m') for i in range(5, -1, -1)]


    positive_counts = []
    negative_counts = []


    for month in months:
        start_date = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30 * (5 - months.index(month)))
        end_date = start_date + timedelta(days=30)

        positive_counts.append(PredictionDiabete.objects.filter(date_prediction__range=[start_date, end_date], resultat=True).count())
        negative_counts.append(PredictionDiabete.objects.filter(date_prediction__range=[start_date, end_date], resultat=False).count())

    data = {
        "labels": months,
        "positive_counts": positive_counts,
        "negative_counts": negative_counts,
    }

    return JsonResponse(data)
