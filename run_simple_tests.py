import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from users.models import Subscription
from django.urls import reverse

User = get_user_model()

class SimpleAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            course=self.course,
            owner=self.user
        )
    def test_course_list(self):
        """Тест списка курсов"""
        url = reverse('course-list')
        response = self.client.get(url)
        print(f"✅ Course list: {response.status_code}")
        self.assertEqual(response.status_code, 200)
    
    def test_lesson_list(self):
        """Тест списка уроков"""
        url = reverse('lesson-list')
        response = self.client.get(url)
        print(f"✅ Lesson list: {response.status_code}")
        self.assertEqual(response.status_code, 200)
    
    def test_subscription_create(self):
        """Тест создания подписки"""
        url = reverse('subscriptions')
        response = self.client.post(url, {'course_id': self.course.id})
        print(f"✅ Subscription create: {response.status_code}")
        self.assertIn(response.status_code, [200, 201])

from rest_framework.test import APIClient

print("=== Запуск простых тестов ===")
test = SimpleAPITest()
test.setUp()
test.test_course_list()
test.test_lesson_list()
test.test_subscription_create()
print("=== Тесты завершены ===")
