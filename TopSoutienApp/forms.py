from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import User, StudentProfile, TeacherProfile

class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé acceptant email ou téléphone
    """
    username = forms.CharField(
        label='Email ou Téléphone',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre email ou numéro de téléphone'
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Vérifier si c'est un email ou un téléphone
        if '@' in username:
            # C'est un email
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                raise ValidationError('Aucun utilisateur trouvé avec cet email.')
        else:
            # C'est un téléphone
            try:
                user = User.objects.get(phone_number=username)
                return user.username
            except User.DoesNotExist:
                raise ValidationError('Aucun utilisateur trouvé avec ce numéro de téléphone.')
    
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_active:
            raise ValidationError('Ce compte a été désactivé.')


class StudentSignUpForm(UserCreationForm):
    """
    Formulaire d'inscription pour les étudiants - basé sur signup_student.html
    """
    # Champs du template signup_student.html
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre prénom',
            'id': 'firstname'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom',
            'id': 'lastname'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemple@email.com',
            'id': 'email'
        })
    )
    phone_number = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Numéro de téléphone',
            'id': 'phone'
        })
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control d-none',
            'id': 'photo',
            'accept': 'image/*'
        })
    )
    
    # Champs de mot de passe
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe',
            'id': 'password1'
        }),
        help_text='Votre mot de passe doit contenir au moins 8 caractères.'
    )
    password2 = forms.CharField(
        label='Confirmation du mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe',
            'id': 'password2'
        }),
        help_text='Entrez le même mot de passe que précédemment, pour vérification.'
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Un utilisateur avec cet email existe déjà.')
        return email
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone).exists():
            raise ValidationError('Un utilisateur avec ce numéro de téléphone existe déjà.')
        return phone
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        
        if len(password1) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'student'
        user.username = self.cleaned_data['email']  # Utiliser l'email comme username
        
        if commit:
            user.save()
            # Créer le profil étudiant
            StudentProfile.objects.create(user=user)
        return user


class TeacherSignUpForm(UserCreationForm):
    """
    Formulaire d'inscription pour les professeurs - basé sur signup_teacher.html
    """
    # Champs du template signup_teacher.html
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre prénom'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemple@email.com',
            'id': 'email'
        })
    )
    phone_number = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Numéro de téléphone',
            'id': 'phone'
        })
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control d-none',
            'id': 'photo',
            'accept': 'image/*'
        })
    )
    
    # Champs de mot de passe
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe',
            'id': 'password1'
        }),
        help_text='Votre mot de passe doit contenir au moins 8 caractères.'
    )
    password2 = forms.CharField(
        label='Confirmation du mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe',
            'id': 'password2'
        }),
        help_text='Entrez le même mot de passe que précédemment, pour vérification.'
    )
    
    # Champs spécifiques aux professeurs du template
    domains_of_competence = forms.ChoiceField(
        choices=TeacherProfile.DOMAIN_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'competence'
        }),
        help_text='Sélectionnez votre domaine de compétence'
    )
    cv_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control d-none',
            'id': 'cv',
            'accept': 'application/pdf'
        })
    )
    presentation_video = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control d-none',
            'id': 'video',
            'accept': 'video/*'
        })
    )
    bio = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Présentez-vous en quelques lignes...',
            'id': 'bio',
            'rows': 3
        })
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Un utilisateur avec cet email existe déjà.')
        return email
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone).exists():
            raise ValidationError('Un utilisateur avec ce numéro de téléphone existe déjà.')
        return phone
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        
        # Validation de la force du mot de passe
        if len(password1) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'teacher'
        user.username = self.cleaned_data['email']  # Utiliser l'email comme username
        
        if commit:
            user.save()
            # Créer le profil professeur
            TeacherProfile.objects.create(
                user=user,
                domains_of_competence=self.cleaned_data['domains_of_competence'],
                bio=self.cleaned_data['bio'],
            )
        return user 


class PaymentForm(forms.Form):
    """
    Formulaire de paiement Mobile Money
    """
    phone_number = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre numéro Mobile Money (ex: +241 01 23 45 67)',
            'id': 'phone_number'
        }),
        help_text='Entrez votre numéro de téléphone associé à votre compte Mobile Money'
    )
    
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=0,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'id': 'amount'
        }),
        help_text='Montant à prélever (FCFA)'
    )
    
    payment_method = forms.ChoiceField(
        choices=[
            ('mobile_money', 'Mobile Money'),
            ('orange_money', 'Orange Money'),
            ('moov_money', 'Moov Money'),
        ],
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'payment-method-radio'
        }),
        initial='mobile_money'
    )
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # Validation basique du numéro de téléphone
        if not phone.startswith('+'):
            phone = '+' + phone
        return phone 