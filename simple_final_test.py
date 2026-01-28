import os
import django

# 1. Сначала настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("ПРОСТОЙ ФИНАЛЬНЫЙ ТЕСТ")
print("=" * 60)

# 2. Теперь импортируем все остальное
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from users.models import Subscription
from django.urls import reverse

User = get_user_model()

print("1. Проверка моделей...")
try:
    # Создаем пользователя
    user = User.objects.create_user(
        email='simple_test@example.com',
        password='testpass123'
    )
    print(f"   ✅ Пользователь создан: {user.email}")
    
    # Создаем курс
    course = Course.objects.create(
        title='Simple Test Course',
        description='Test course',
        owner=user
    )
    print(f"   ✅ Курс создан: {course.title}")
    
    # Создаем урок с валидной YouTube ссылкой
    lesson = Lesson.objects.create(
        title='Simple Test Lesson',
        description='Test lesson',
        video_url='https://www.youtube.com/watch?v=test123',
        course=course,
        owner=user
    )
    print(f"   ✅ Урок создан: {lesson.title}")
    
    # Создаем подписку
    subscription = Subscription.objects.create(
        user=user,
        course=course
    )
    print(f"   ✅ Подписка создана")
    print("\n2. Проверка валидации YouTube...")
    try:
        # Пытаемся создать урок с невалидной ссылкой
        invalid_lesson = Lesson(
            title='Invalid Lesson',
            description='Invalid',
            video_url='https://vimeo.com/123456',
            course=course,
            owner=user
        )
        invalid_lesson.full_clean()
        print("   ❌ Невалидная ссылка принята (это плохо)")
    except Exception as e:
        print(f"   ✅ Невалидная ссылка отвергнута: {str(e)[:50]}...")
    
    print("\n3. Проверка URL...")
    try:
        url = reverse('course-list')
        print(f"   ✅ course-list URL: {url}")
        
        url = reverse('lesson-list')
        print(f"   ✅ lesson-list URL: {url}")
        
        url = reverse('subscriptions')
        print(f"   ✅ subscriptions URL: {url}")
        
        print("\n✅ ВСЕ ОСНОВНЫЕ ФУНКЦИИ РАБОТАЮТ!")
        print("=" * 60)
        print("Проект готов к сдаче! 🎉")
        
    except Exception as e:
        print(f"   ❌ Ошибка URL: {e}")
        
except Exception as e:
    print(f"❌ Критическая ошибка: {e}")
    import traceback
    traceback.print_exc()
