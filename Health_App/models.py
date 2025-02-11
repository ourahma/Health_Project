from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model

# Custom Manager to handle login permissions
class PersonneManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Base class
class Personne(AbstractBaseUser, PermissionsMixin):
    username = None  # Remove default username field
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nom", "prenom"]

    objects = PersonneManager()
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="personne_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="personne_permissions",
        blank=True
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)
    objects = PersonneManager() 
    
    def is_medcin(self):
        return self.is_superuser 


# Patient ne ppeut pas faire login mais herite de Personne
class Patient(Personne):
    adresse = models.CharField(max_length=255, null=True, blank=True)
    cni= models.CharField(max_length=20, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)

    
    def save(self, *args, **kwargs):
        self.is_active = False  # Prevent login
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.cni}"

# Medcin Peut faite log in 
class Medcin(Personne):
    specialite = models.CharField(max_length=100)
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_staff = True
        super().save(*args, **kwargs)
def get_default_medcin():
    return Medcin.objects.first() 
# Secretaire 
class Secretaire(models.Model): 
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="secretaire_profile")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    medcin = models.ForeignKey(Medcin, on_delete=models.CASCADE)
    phone_number= models.CharField(max_length=15, null=True, blank=True)
    def __str__(self):
        return f"Secretaire {self.user.nom} {self.user.prenom}"



class Maladie(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    symptoms = models.TextField(help_text="Liste de symptômes séparés par des virgules")
    traitements = models.TextField(help_text="Liste de traitements séparés par des virgules")

    def get_symptoms_list(self):
        """Retourne la liste des symptômes."""
        return self.symptoms.split(",") if self.symptoms else []

    def set_symptoms_list(self, symptoms_list):
        """Met à jour la liste des symptômes."""
        if isinstance(symptoms_list, list) and all(isinstance(item, str) for item in symptoms_list):
            self.symptoms = ",".join(symptoms_list)
        else:
            raise ValueError("Les symptômes doivent être une liste de chaînes de caractères.")

    def get_traitements_list(self):
        """Retourne la liste des traitements."""
        return self.traitements.split(",") if self.traitements else []

    def set_traitements_list(self, traitements_list):
        """Met à jour la liste des traitements."""
        if isinstance(traitements_list, list) and all(isinstance(item, str) for item in traitements_list):
            self.traitements = ",".join(traitements_list)
        else:
            raise ValueError("Les traitements doivent être une liste de chaînes de caractères.")

    def _str_(self):
        return self.nom
    
    @classmethod
    def search_by_nom(cls, search_term):
        
        return cls.objects.filter(nom__icontains=search_term)



class Rendezvous(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()  
    status = models.CharField(max_length=20, default='en attente')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)

    def _str_(self):
        return f"Rendez-vous {self.id} - {self.patient.nom} {self.patient.prenom}"

# Modèle de Consultation
class Consultation(models.Model):
    id = models.AutoField(primary_key=True)
    is_validate = models.BooleanField(default=False)
    maladie = models.ForeignKey('Maladie', on_delete=models.SET_NULL, null=True, blank=True, related_name="consultations")
    montant = models.FloatField()
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name="consultations")
    rendez_vous = models.OneToOneField('RendezVous', on_delete=models.CASCADE, related_name="consultation")

    def _str_(self):
        return f"Consultation {self.id} - {self.patient.nom} {self.patient.maladie}"
    
    
    
## stocker l'historique de la prediction
class PredictionDiabete(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="predictions")
    glucose = models.FloatField()
    insuline = models.FloatField()
    bmi = models.FloatField()
    age = models.IntegerField()
    resultat = models.BooleanField()  # 0 = Pas de diabète, 1 = Diabète détecté
    date_prediction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prédiction {self.id} - {self.patient.nom} - {'Diabétique' if self.resultat else 'Non diabétique'}"

class PredictionMaladieHistorique(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="predictions_maladie")
    maladie_predite = models.CharField(max_length=255)
    date_prediction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prédiction {self.id} - {self.patient.nom} - {self.maladie_predite}"
