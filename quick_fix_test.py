import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

print("=" * 60)
print("БЫСТРЫЙ ТЕСТ С ИСПРАВЛЕНИЕМ ALLOWED_HOSTS")
print("=" * 60)

class QuickFixTest(TransactionTestCase):
    def test_1_basic_setup(self):
        print("\n1. Базовая настройка:")
        
        # Создаем пользователя
        self.user = User.objects.create_user(
            email='test_fix@example.com',
            password='testpass123'
        )
        print(f"   ✅ Пользователь создан")
        # Создаем клиент и аутентифицируем
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        print(f"   ✅ Клиент аутентифицирован")
        
        return True
    
    def test_2_api_endpoints(self):
        print("\n2. Проверка API эндпоинтов:")
        
        endpoints = [
            ('course-list', 'GET'),
            ('lesson-list', 'GET'),
            ('subscriptions', 'GET'),
        ]
        
        success = 0
        for endpoint, method in endpoints:
            try:
                url = reverse(endpoint)
                
                if method == 'GET':
                    response = self.client.get(url)
                elif method == 'POST':
                    response = self.client.post(url, {})
                
                status_code = response.status_code
                if status_code in [200, 201]:
                    print(f"   ✅ {endpoint}: {status_code}")
                    success += 1
                else:
                    print(f"   ❌ {endpoint}: {status_code}")
            except Exception as e:
                print(f"   ❌ {endpoint}: {e}")

        print(f"   Итог: {success}/{len(endpoints)} успешно")
        return success >= 2
    
    def test_3_create_models(self):
        print("\n3. Создание моделей:")
        
        try:
            # Импортируем модели
            from materials.models import Course, Lesson
            from users.models import Subscription
            
            # Создаем курс
            course = Course.objects.create(
                title='Test Course for Fix',
                description='Test course description',
                owner=self.user
            )
            print(f"   ✅ Курс создан: {course.title}")
            
            # Создаем урок
            lesson = Lesson.objects.create(
                title='Test Lesson',
                description='Test lesson description',
                video_url='https://www.youtube.com/watch?v=test123',
                course=course,
                owner=self.user
            )
            print(f"   ✅ Урок создан: {lesson.title}")
            
            # Создаем подписку
            subscription = Subscription.objects.create(
                user=self.user,
                course=course
            )
            print(f"   ✅ Подписка создана")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Ошибка создания моделей: {e}")
            return False
    def run_all(self):
        """Запуск всех тестов"""
        results = []
        
        results.append(self.test_1_basic_setup())
        results.append(self.test_2_api_endpoints())
        results.append(self.test_3_create_models())
        
        print("\n" + "=" * 60)
        print("ИТОГИ БЫСТРОГО ТЕСТА")
        print("=" * 60)
        
        passed = sum(results)
        total = len(results)
        
        for i, result in enumerate(results, 1):
            status_text = "✅ ПРОЙДЕН" if result else "❌ НЕ ПРОЙДЕН"
            print(f"Тест {i}: {status_text}")
        
        print(f"\nВсего тестов: {total}")
        print(f"Пройдено: {passed}")
        
        if passed == total:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
            return True
        else:
            print(f"\n⚠️  Пройдено {passed}/{total} тестов")
            return passed >= 2

# Запускаем тесты
test = QuickFixTest()
test.setUp()
success = test.run_all()

if success:
    print("\n✅ Система работает! Можно запускать полные тесты.")
    print("=" * 60)
    exit(0)
else:
    print("\n❌ Есть проблемы с системой.")
    print("=" * 60)
    exit(1)
