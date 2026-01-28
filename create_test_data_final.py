import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from users.models import Subscription

User = get_user_model()

print("=== Создание тестовых данных ===\n")

# Создаем пользователей
users_data = [
    {'email': 'owner@example.com', 'first_name': 'Owner', 'last_name': 'User'},
    {'email': 'student@example.com', 'first_name': 'Student', 'last_name': 'User'},
]

for user_data in users_data:
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults=user_data
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f"✅ Создан пользователь: {user.email}")
    else:
        print(f"✅ Пользователь уже существует: {user.email}")

# Создаем курс
owner = User.objects.get(email='owner@example.com')
course, created = Course.objects.get_or_create(
    title='Python для начинающих',
    defaults={
        'description': 'Курс по основам программирования на Python',
        'owner': owner
    }
)
print(f"✅ Курс: {course.title}")
# Создаем уроки
lessons_data = [
    {
        'title': 'Введение в Python',
        'description': 'Основные понятия языка Python',
        'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'course': course,
        'owner': owner
    },
    {
        'title': 'Переменные и типы данных',
        'description': 'Работа с переменными и основными типами данных',
        'video_url': 'https://youtu.be/dQw4w9WgXcQ',
        'course': course,
        'owner': owner
    },
]

for lesson_data in lessons_data:
    lesson, created = Lesson.objects.get_or_create(
        title=lesson_data['title'],
        defaults=lesson_data
    )
    print(f"✅ Урок: {lesson.title}")
# Создаем подписку
student = User.objects.get(email='student@example.com')
subscription, created = Subscription.objects.get_or_create(
    user=student,
    course=course
)
print(f"✅ Подписка: {student.email} → {course.title}")

print("\n=== Тестовые данные созданы ===")

# Выводим статистику
print(f"\nСтатистика:")
print(f"- Пользователей: {User.objects.count()}")
print(f"- Курсов: {Course.objects.count()}")
print(f"- Уроков: {Lesson.objects.count()}")
print(f"- Подписок: {Subscription.objects.count()}")
