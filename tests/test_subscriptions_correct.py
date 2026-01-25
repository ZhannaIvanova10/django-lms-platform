from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from materials.models import Course, Subscription


class SubscriptionCorrectTests(TestCase):
    """Правильные тесты подписок с использованием course_id"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='correcttest@example.com',
            password='test123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.course = Course.objects.create(
            title='Correct Test Course',
            description='Course for correct tests',
            owner=self.user
        )
    def test_create_subscription_with_course_id(self):
        """Тест создания подписки с правильным полем course_id"""
        print("\n🧪 Тест создания подписки с course_id:")
        
        url = reverse('subscriptions')
        
        # Правильный запрос с course_id
        data = {'course_id': self.course.id}
        print(f"   Данные: {data}")
        
        response = self.client.post(url, data, format='json')
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.data}")
        
        # Должен быть 200 OK (а не 201)
        self.assertEqual(response.status_code, 200)
        
        # Проверяем сообщение
        self.assertIn('message', response.data)
        self.assertTrue(response.data['is_subscribed'])
        print(f"   ✅ {response.data['message']}")
        
        # Проверяем что подписка создана в БД
        self.assertEqual(Subscription.objects.count(), 1)
        subscription = Subscription.objects.first()
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, self.course)
        print(f"   ✅ Подписка создана в БД")
    def test_delete_subscription(self):
        """Тест удаления подписки"""
        print("\n🧪 Тест удаления подписки:")
        
        url = reverse('subscriptions')
        
        # Сначала создаем подписку
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        print(f"   Создание: {response.data['message']}")
        
        # Теперь удаляем (повторный POST с тем же course_id)
        response = self.client.post(url, data, format='json')
        print(f"   Удаление: статус {response.status_code}")
        print(f"   Ответ: {response.data}")
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['is_subscribed'])
        print(f"   ✅ {response.data['message']}")
        
        # Проверяем что подписка удалена из БД
        self.assertEqual(Subscription.objects.count(), 0)
        print(f"   ✅ Подписка удалена из БД")
    
    def test_get_subscriptions_list(self):
        """Тест получения списка подписок"""
        print("\n🧪 Тест списка подписок:")
        url = reverse('subscriptions')
        
        # Создаем несколько подписок
        courses = []
        for i in range(3):
            course = Course.objects.create(
                title=f'Course {i}',
                description=f'Description {i}',
                owner=self.user
            )
            courses.append(course)
            
            # Создаем подписку
            self.client.post(url, {'course_id': course.id}, format='json')
            print(f"   Создана подписка на курс {i}")
        
        # Получаем список подписок
        response = self.client.get(url)
        print(f"   GET список: статус {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        print(f"   ✅ Получено {len(response.data)} подписок")
        
        # Проверяем структуру данных
        for subscription in response.data:
            self.assertIn('id', subscription)
            self.assertIn('user', subscription)
            self.assertIn('course', subscription)
            self.assertIn('is_active', subscription)
        print(f"   ✅ Структура данных корректна")
    
    def test_error_cases(self):
        """Тест обработки ошибок"""
        print("\n🧪 Тест ошибок:")

        url = reverse('subscriptions')
        
        # 1. Без course_id
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'course_id обязателен')
        print(f"   ✅ Ошибка без course_id: {response.data['error']}")
        
        # 2. С несуществующим course_id
        response = self.client.post(url, {'course_id': 9999}, format='json')
        self.assertEqual(response.status_code, 404)
        print(f"   ✅ Несуществующий курс: статус 404")
        
        # 3. GET без аутентификации
        client = APIClient()  # Новый клиент без аутентификации
        response = client.get(url)
        self.assertEqual(response.status_code, 401)
        print(f"   ✅ GET без аутентификации: статус 401")
        
        # 4. POST без аутентификации
        response = client.post(url, {'course_id': 1}, format='json')
        self.assertEqual(response.status_code, 401)
        print(f"   ✅ POST без аутентификации: статус 401")
    
    def runTest(self):
        """Запуск всех тестов"""
        print("=" * 60)
        print("ТЕСТЫ ПОДПИСОК С ПРАВИЛЬНЫМ API")
        print("=" * 60)
        self.test_create_subscription_with_course_id()
        self.test_delete_subscription()
        self.test_get_subscriptions_list()
        self.test_error_cases()
        
        print("\n" + "=" * 60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 60)
