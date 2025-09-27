from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomAuthenticationForm, StudentSignUpForm, TeacherSignUpForm, PaymentForm
from datetime import datetime, timedelta

# Templates constants (ENGLISH)
LOGIN_TEMPLATE = 'TopSoutienApp/login.html'
HOME_TEMPLATE = 'TopSoutienApp/home.html'
FIND_TEACHER_TEMPLATE = 'TopSoutienApp/find_teacher.html'
COURSE_BOOKING_TEMPLATE = 'TopSoutienApp/course_booking.html'
TEACHER_SIGNUP_TEMPLATE = 'TopSoutienApp/signup_teacher.html'
STUDENT_SIGNUP_TEMPLATE = 'TopSoutienApp/signup_student.html'
STUDENT_PROFILE_TEMPLATE = 'TopSoutienApp/student_profile.html'
TEACHER_PROFILE_TEMPLATE = 'TopSoutienApp/teacher_profile.html'
JOIN_COURSE_TEMPLATE = 'TopSoutienApp/join_course.html'


def login_view(request: HttpRequest) -> HttpResponse:
    """Display the login page with authentication."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.get_full_name()}!')
                
                # Rediriger selon le type d'utilisateur
                if user.user_type == 'admin':
                    return redirect('admin_page')
                elif user.user_type == 'teacher':
                    return redirect('teacher_profile')
                else:  # student
                    return redirect('student_profile')
            else:
                messages.error(request, 'Email/téléphone ou mot de passe incorrect.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, LOGIN_TEMPLATE, {'form': form})


def signup_student(request: HttpRequest) -> HttpResponse:
    """Display and handle student signup."""
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.get_full_name()}! Votre compte étudiant a été créé avec succès.')
            return redirect('student_profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = StudentSignUpForm()
    
    return render(request, STUDENT_SIGNUP_TEMPLATE, {'form': form})


def signup_teacher(request: HttpRequest) -> HttpResponse:
    """Display and handle teacher signup."""
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.get_full_name()}! Votre compte professeur a été créé avec succès.')
            return redirect('teacher_profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = TeacherSignUpForm()
    
    return render(request, TEACHER_SIGNUP_TEMPLATE, {'form': form})


@login_required
def student_profile(request: HttpRequest) -> HttpResponse:
    """Display the student profile page with user data."""
    user = request.user
    if user.user_type != 'student':
        messages.error(request, 'Accès non autorisé.')
        return redirect('home')
    
    context = {
        'user': user,
        'student_profile': getattr(user, 'student_profile', None),
        'full_name': user.get_full_name(),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone_number': user.phone_number,
        'profile_picture': user.profile_picture,
        'user_type': user.get_user_type_display(),  # Affiche "Étudiant" au lieu de "student"
    }
    return render(request, STUDENT_PROFILE_TEMPLATE, context)


@login_required
def teacher_profile(request: HttpRequest) -> HttpResponse:
    """Display the teacher profile page with user data."""
    user = request.user
    if user.user_type != 'teacher':
        messages.error(request, 'Accès non autorisé.')
        return redirect('home')
    
    teacher_profile = getattr(user, 'teacher_profile', None)
    
    context = {
        'user': user,
        'teacher_profile': teacher_profile,
        'full_name': user.get_full_name(),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone_number': user.phone_number,
        'profile_picture': user.profile_picture,
        'user_type': user.get_user_type_display(),  # Affiche "Professeur" au lieu de "teacher"
        'domains_of_competence': teacher_profile.domains_of_competence if teacher_profile else None,
        'bio': teacher_profile.bio if teacher_profile else None,
        'cv_file': teacher_profile.cv_file if teacher_profile else None,
        'presentation_video': teacher_profile.presentation_video if teacher_profile else None,
    }
    return render(request, TEACHER_PROFILE_TEMPLATE, context)


def home(request: HttpRequest) -> HttpResponse:
    """Display the home page."""
    return render(request, HOME_TEMPLATE)


@login_required
def find_teacher(request: HttpRequest) -> HttpResponse:
    """Display the teacher search page - accessible only to authenticated users."""
    return render(request, FIND_TEACHER_TEMPLATE, {'user': request.user})


@login_required
def course_booking(request):
    """Display the course booking page - accessible only to authenticated users."""
    time_slots = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]
    today = datetime.today()
    available_dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    context = {
        'time_slots': time_slots,
        'available_dates': available_dates,
        'prof': {
            'name': 'Dr. Sophie Dupont',
            'photo': '/static/img/prof.jpg',
            'bio': "Experienced teacher in mathematics and sciences for 12 years.",
        },
        'user': request.user
    }
    return render(request, COURSE_BOOKING_TEMPLATE, context)


def join_course(request):
    """Display a prototype video call room (front-end only)."""
    return render(request, JOIN_COURSE_TEMPLATE)


def admin_page(request):
    """Display the admin dashboard page."""
    return render(request, 'TopSoutienApp/admin_page.html')


@login_required
def payment_page(request):
    """Page de paiement accessible uniquement aux utilisateurs connectés."""
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Ici on traiterait le paiement réel
            phone_number = form.cleaned_data['phone_number']
            amount = form.cleaned_data['amount']
            
            # Simulation du paiement
            messages.success(request, f'Paiement de {amount} FCFA effectué avec succès via Mobile Money ({phone_number})!')
            return redirect('student_profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        # Récupérer les données du cours depuis la session ou les paramètres
        course_data = request.session.get('course_data', {
            'prof_name': 'Dr. Sophie Dupont',
            'subject': 'Mathématiques',
            'duration': '1h30',
            'date': '2025-01-25',
            'time': '14:00',
            'amount': 5000  # Prix par défaut
        })
        
        form = PaymentForm(initial={'amount': course_data['amount']})
    
    context = {
        'user': request.user,
        'form': form,
        'course_data': request.session.get('course_data', {
            'prof_name': 'Dr. Sophie Dupont',
            'subject': 'Mathématiques',
            'duration': '1h30',
            'date': '2025-01-25',
            'time': '14:00',
            'amount': 5000
        })
    }
    return render(request, 'TopSoutienApp/payment.html', context)





