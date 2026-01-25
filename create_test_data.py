import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User, Payment
from materials.models import Course, Lesson

def create_test_data():
    """Создание тестовых данных для платежей"""
    
    print("Создание тестовых данных...")
    
    # Создаем тестового пользователя если нет
    user, created = User.objects.get_or_create(
        email='student@example.com',
        defaults={
            'first_name': 'Иван',
            'last_name': 'Студент',
            'phone': '+79991234567',
            'city': 'Москва'
        }
    )
    if created:
        user.set_password('Student123!')
        user.save()
        print(f"Создан пользователь: {user.email}")
    else:
        print(f"Используем существующего пользователя: {user.email}")
    # Получаем или создаем курсы
    courses = []
    for i in range(1, 4):
        course, _ = Course.objects.get_or_create(
            title=f'Курс {i}',
            defaults={
                'description': f'Описание курса {i}'
            }
        )
        courses.append(course)
        print(f"Курс: {course.title}")
    
    # Создаем уроки
    lessons = []
    for course in courses:
        for j in range(1, 4):
            lesson, _ = Lesson.objects.get_or_create(
                title=f'Урок {j} курса {course.title}',
                course=course,
                defaults={
                    'description': f'Описание урока {j}',
                    'video_link': f'https://youtube.com/lesson{j}'
                }
            )
            lessons.append(lesson)
            print(f"Урок: {lesson.title}")
    
    # Создаем платежи (Задание 2)
    payment_methods = ['cash', 'transfer']
    
    for i in range(10):
        # Случайно выбираем курс или урок
        if random.choice([True, False]):
            course = random.choice(courses)
            lesson = None
            item_name = course.title
        else:
            lesson = random.choice(lessons)
            course = None
            item_name = lesson.title

        # Создаем платеж
        payment = Payment.objects.create(
            user=user,
            course=course,
            lesson=lesson,
            amount=random.uniform(1000, 10000),
            payment_method=random.choice(payment_methods),
            payment_date=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        print(f"Создан платеж: {payment.user.email} - {item_name} - {payment.amount:.2f} руб.")
    
    print(f"\n✅ Создано: {User.objects.count()} пользователей")
    print(f"✅ Создано: {Course.objects.count()} курсов")
    print(f"✅ Создано: {Lesson.objects.count()} уроков")
    print(f"✅ Создано: {Payment.objects.count()} платежей")

if __name__ == '__main__':
    create_test_data()
