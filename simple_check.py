import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class SimpleCheck(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test_check@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_basic_urls(self):
        """Проверка базовых URL"""
        print("Проверка URL:")
        
        urls_to_test = [
            'course-list',
            'lesson-list',
            'subscriptions',
        ]
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"  {url_name}: {url}")
            except Exception as e:
                print(f"  ❌ {url_name}: {e}")
    
    def test_create_course(self):
        """Проверка создания курса"""
        print("\nПроверка создания курса:")
        
        from materials.models import Course
        
        course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        
        print(f"  ✅ Курс создан: {course.title}")
        print(f"  Владелец: {course.owner.email}")
        
        # Проверяем API
        url = reverse('course-list')
        response = self.client.get(url)
        print(f"  API статус: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ API работает")
            return True
        else:
            print(f"  ❌ API ошибка: {response.status_code}")
            return False

if __name__ == '__main__':
    print("=" * 50)
    print("ПРОСТАЯ ПРОВЕРКА LMS СИСТЕМЫ")
    print("=" * 50)
    
    checker = SimpleCheck()
    checker.setUp()
    checker.test_basic_urls()
    checker.test_create_course()
    
    print("\n" + "=" * 50)
    print("ПРОВЕРКА ЗАВЕРШЕНА")
    print("=" * 50)
