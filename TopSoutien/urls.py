from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from TopSoutienApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    
    path('login/', login_view, name='login'),
    path('signup-student/', signup_student, name='signup_student'),
    path('signup-teacher/', signup_teacher, name='signup_teacher'),
    path('student-profile/',student_profile, name='student_profile'),
    path('teacher-profile/', teacher_profile, name='teacher_profile'),
    path('find-teacher/', find_teacher, name='find_teacher'),
    path('course-booking/', course_booking, name='course_booking'),
    path('payment/', payment_page, name='payment'),  # Nouvelle URL
    path('join-course/',join_course, name='join_course'),
    path('admin-page/', admin_page, name='admin_page'),
] 

# Ajouter les URLs pour les médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 