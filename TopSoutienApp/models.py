from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec support pour email/téléphone
    """
    USER_TYPE_CHOICES = [
        ('admin', 'Administrateur'),
        ('student', 'Étudiant'),
        ('teacher', 'Professeur'),
    ]
    
    # Champs de base pour tous les utilisateurs
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='student'
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        unique=True
    )
    
    # Champs optionnels
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"
    
    def get_identifier(self):
        """Retourne l'email ou le téléphone pour l'authentification"""
        return self.email or self.phone_number


class StudentProfile(models.Model):
    """
    Profil spécifique aux étudiants - basé sur le template signup_student.html
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
    # Aucun champ spécifique pour l'étudiant dans le template actuel
    # Seulement les champs de base du User (nom, prénom, email, téléphone, photo)
    
    def __str__(self):
        return f"Profil étudiant de {self.user.get_full_name()}"


class TeacherProfile(models.Model):
    """
    Profil spécifique aux professeurs - basé sur le template signup_teacher.html
    """
    DOMAIN_CHOICES = [
        ('mathematiques', 'Mathématiques'),
        ('physique', 'Physique'),
        ('physique_chimie', 'Physique-Chimie'),
        ('svt', 'SVT'),
        ('francais', 'Français'),
        ('anglais', 'Anglais'),
        ('informatique', 'Informatique'),
        ('histoire', 'Histoire'),
        ('histoire_geo', 'Histoire-Géo'),
        ('economie', 'Économie'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    
    # Champs du template signup_teacher.html
    domains_of_competence = models.CharField(
        max_length=20,
        choices=DOMAIN_CHOICES,
        blank=True,
        null=True
    )
    cv_file = models.FileField(upload_to='teacher_cvs/', blank=True, null=True)  # cv
    presentation_video = models.FileField(upload_to='teacher_videos/', blank=True, null=True)  # video
    bio = models.TextField(blank=True, null=True)  # bio
    
    def __str__(self):
        return f"Profil professeur de {self.user.get_full_name()}"
