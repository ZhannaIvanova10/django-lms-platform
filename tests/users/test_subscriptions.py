from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from materials.models import Course, Subscription

User = get_user_model()


class SubscriptionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Course Description',
            owner=self.user
        )
    
    def test_create_subscription(self):
        """Создание подписки"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(
            '/api/subscriptions/',
            {'course_id': self.course.id}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка создана')
        self.assertTrue(response.data['is_subscribed'])
        
        # Проверяем создание в БД
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )
    def test_delete_subscription(self):
        """Удаление подписки"""
        # Сначала создаем подписку
        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(
            '/api/subscriptions/',
            {'course_id': self.course.id}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(response.data['is_subscribed'])
        
        # Проверяем удаление/деактивацию
        subscription.refresh_from_db()
        self.assertFalse(subscription.is_active)
    
    def test_subscription_indicator_in_course(self):
        """Индикатор подписки в данных курса"""
        # Создаем подписку
        Subscription.objects.create(
            user=self.user,
            course=self.course
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(f'/api/courses/{self.course.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])
    
    def test_get_subscriptions_list(self):
        """Получение списка подписок"""
        # Создаем несколько подписок
        course2 = Course.objects.create(
            title='Another Course',
            owner=self.user
        )

        Subscription.objects.create(user=self.user, course=self.course)
        Subscription.objects.create(user=self.user, course=course2)
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/subscriptions/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
