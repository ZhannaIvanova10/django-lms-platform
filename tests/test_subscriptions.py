from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from materials.models import Course, Subscription
from users.models import User


class SubscriptionTestCase(TestCase):
    """
    Тесты для функционала подписок на курсы
    """
    
    def setUp(self):
        """
        Настройка тестовых данных
        """
        # Создаем пользователей
        self.user1 = User.objects.create(
            email='user1@example.com',
            password='password123',
            first_name='User1',
            last_name='Test',
            is_active=True
        )
        self.user2 = User.objects.create(
            email='user2@example.com',
            password='password456',
            first_name='User2',
            last_name='Test',
            is_active=True
        )
        
        # Создаем курсы
        self.course1 = Course.objects.create(
            title='Course 1',
            description='Description 1',
            owner=self.user1
        )
        
        self.course2 = Course.objects.create(
            title='Course 2',
            description='Description 2',
            owner=self.user2
        )
        
        # Создаем клиенты API
        self.client1 = APIClient()
        self.client2 = APIClient()
        
        # Аутентифицируем клиентов
        self.client1.force_authenticate(user=self.user1)
        self.client2.force_authenticate(user=self.user2)
    
    def test_add_subscription(self):
        """
        Тест добавления подписки на курс
        """
        url = reverse('subscriptions')
        data = {'course_id': self.course2.id}

        # Пользователь 1 подписывается на курс пользователя 2
        response = self.client1.post(url, data)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['message'],
            'Подписка добавлена'
        )
        self.assertTrue(
            response.data['is_subscribed']
        )
        
        # Проверяем, что подписка создалась в базе
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user1,
                course=self.course2
            ).exists()
        )
    
    def test_remove_subscription(self):
        """
        Тест удаления подписки
        """
        # Сначала создаем подписку
        Subscription.objects.create(
            user=self.user1,
            course=self.course2
        )
        url = reverse('subscriptions')
        data = {'course_id': self.course2.id}
        
        # Удаляем подписку
        response = self.client1.post(url, data)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['message'],
            'Подписка удалена'
        )
        self.assertFalse(
            response.data['is_subscribed']
        )
        
        # Проверяем, что подписки больше нет
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user1,
                course=self.course2
            ).exists()
        )
    
    def test_toggle_subscription(self):
        """
        Тест переключения подписки (добавить/удалить)
        """
        url = reverse('subscriptions')
        data = {'course_id': self.course1.id}
        # Первый запрос - добавляем подписку
        response1 = self.client2.post(url, data)
        self.assertEqual(
            response1.data['message'],
            'Подписка добавлена'
        )
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user2,
                course=self.course1
            ).exists()
        )
        
        # Второй запрос - удаляем подписку
        response2 = self.client2.post(url, data)
        self.assertEqual(
            response2.data['message'],
            'Подписка удалена'
        )
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user2,
                course=self.course1
            ).exists()
        )
    
    def test_get_subscriptions_list(self):
        """
        Тест получения списка подписок пользователя
        """
        # Создаем несколько подписок
        Subscription.objects.create(user=self.user1, course=self.course1)
        Subscription.objects.create(user=self.user1, course=self.course2)
        
        url = reverse('subscriptions')
        response = self.client1.get(url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['count'],
            2
        )
        self.assertEqual(
            len(response.data['results']),
            2
        )
    
    def test_subscription_field_in_course(self):
        """
        Тест поля is_subscribed в сериализаторе курса
        """
        # Пользователь 2 подписывается на курс 1
        Subscription.objects.create(
            user=self.user2,
            course=self.course1
        )
        # Получаем детальную информацию о курсе 1 для пользователя 2
        url = reverse('course-detail', args=[self.course1.id])
        response = self.client2.get(url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertTrue(
            response.data['is_subscribed']
        )
        
        # Для пользователя 1 (владельца курса, но не подписчика)
        url = reverse('course-detail', args=[self.course1.id])
        response = self.client1.get(url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertFalse(
            response.data['is_subscribed']
        )
    
    def test_subscription_unique_constraint(self):
        """
        Тест уникальности подписки (один пользователь - одна подписка на курс)
        """
        # Создаем первую подписку
        Subscription.objects.create(
            user=self.user1,
            course=self.course2
        )

        # Пытаемся создать вторую подписку (должно вызвать ошибку)
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Subscription.objects.create(
                user=self.user1,
                course=self.course2
            )
    
    def test_subscription_invalid_course(self):
        """
        Тест попытки подписки на несуществующий курс
        """
        url = reverse('subscriptions')
        data = {'course_id': 99999}  # Несуществующий ID
        
        response = self.client1.post(url, data)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
    
    def test_subscription_missing_course_id(self):
        """
        Тест запроса без course_id
        """
        url = reverse('subscriptions')
        data = {}  # Нет course_id
        
        response = self.client1.post(url, data)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            'error',
            response.data
        )
