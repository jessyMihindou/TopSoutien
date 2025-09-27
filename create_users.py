import os
import django

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TopSoutien.settings')
django.setup()

from TopSoutienApp.models import User
from django.contrib.auth.hashers import make_password

def create_test_users():
    # Créer un étudiant
    student = User.objects.create(
        username='etudiant@test.com',
        email='etudiant@test.com',
        phone_number='+33612345678',
        first_name='Jean',
        last_name='Dupont',
        user_type='student',
        password=make_password('password123'),
        is_active=True
    )

    # Créer un professeur
    teacher = User.objects.create(
        username='prof@test.com',
        email='prof@test.com',
        phone_number='+33687654321',
        first_name='Marie',
        last_name='Martin',
        user_type='teacher',
        password=make_password('password123'),
        is_active=True
    )

    print("Utilisateurs créés avec succès!")
    print(f"Étudiant: {student.email} / password123")
    print(f"Professeur: {teacher.email} / password123")

if __name__ == '__main__':
    create_test_users() 