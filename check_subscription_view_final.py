import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🔍 ФИНАЛЬНАЯ ПРОВЕРКА SUBSCRIPTIONVIEW:")

from materials.views import SubscriptionAPIView
from materials.serializers import SubscriptionSerializer

print(f"1. Класс: {SubscriptionAPIView}")
print(f"2. serializer_class: {SubscriptionAPIView.serializer_class}")
print(f"3. permission_classes: {SubscriptionAPIView.permission_classes}")

# Проверяем методы
print(f"\n4. Методы класса:")
import inspect
methods = inspect.getmembers(SubscriptionAPIView, predicate=inspect.isfunction)
for name, method in methods:
    if not name.startswith('_'):
        print(f"   - {name}()")

# Тестируем создание подписки
print(f"\n5. Тестовый запрос:")
from rest_framework.test import APIRequestFactory
from users.models import User
from materials.models import Course

user = User.objects.create_user(email='testview@example.com', password='test123')
course = Course.objects.create(title='Test View Course', description='Test', owner=user)

factory = APIRequestFactory()
request = factory.post('/api/subscriptions/', {'course_id': course.id}, format='json')
request.user = user

view = SubscriptionAPIView()

print(f"   Пользователь: {user.email}")
print(f"   Курс ID: {course.id}")

try:
    # Тестируем POST
    response = view.post(request)
    print(f"   POST статус: {response.status_code}")
    print(f"   POST ответ: {response.data}")
    
    # Тестируем GET
    request.method = 'GET'
    response = view.get(request)
    print(f"   GET статус: {response.status_code}")
    print(f"   GET количество подписок: {len(response.data)}")
    
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Проверка завершена")
