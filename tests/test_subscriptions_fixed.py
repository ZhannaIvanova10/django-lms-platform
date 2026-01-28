from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

from materials.models import Course
from users.models import Subscription  # Исправленный импорт

User = get_user_model()

class SubscriptionTestCase(TestCase):
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
    
    def test_add_subscription(self):
        """Тест добавления подписки на курс"""
        url = reverse('subscriptions')
        response = self.client.post(url, {'course_id': self.course.id})
        
        if response.status_code == 200:
            # Подписка создана
            self.assertTrue(
                Subscription.objects.filter(user=self.user, course=self.course).exists()
            )
        elif response.status_code == 201:
            # Подписка создана (альтернативный код)
            self.assertTrue(
                Subscription.objects.filter(user=self.user, course=self.course).exists()
            )
        else:
            self.fail(f"Unexpected status code: {response.status_code}")

    def test_remove_subscription(self):
        """Тест удаления подписки"""
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)
        
        url = reverse('subscriptions')
        response = self.client.post(url, {'course_id': self.course.id})
        
        # Должно удалить подписку
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
    
    def test_get_subscriptions_list(self):
        """Тест получения списка подписок пользователя"""
        # Создаем подписку
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        
        url = reverse('subscriptions')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
