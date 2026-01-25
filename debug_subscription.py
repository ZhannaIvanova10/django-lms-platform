import os
import django
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from materials.models import Course
from materials.views import SubscriptionAPIView
from rest_framework.test import APIRequestFactory

# Создаем тестовые данные
user = User.objects.create_user(email='debug@test.com', password='test123')
course = Course.objects.create(title='Debug Course', description='Test', owner=user)

print("🔍 ОТЛАДКА СОЗДАНИЯ ПОДПИСКИ:")
print(f"Пользователь: {user.email}")
print(f"Курс: {course.title} (ID: {course.id})")
print(f"Владелец курса: {course.owner.email}")
# Создаем запрос
factory = APIRequestFactory()
request = factory.post('/api/subscriptions/', {
    'course': course.id,
    'is_active': True
}, format='json')
request.user = user

# Проверяем view
try:
    view = SubscriptionAPIView()
    view.request = request
    view.format_kwarg = None
    
    # Пытаемся создать
    from materials.serializers import SubscriptionSerializer
    serializer = SubscriptionSerializer(data=request.data, context={'request': request})
    
    print("\n📋 Проверка сериализатора:")
    print(f"  Данные валидны: {serializer.is_valid()}")
    if not serializer.is_valid():
        print(f"  Ошибки валидации: {serializer.errors}")
    else:
        print(f"  Валидированные данные: {serializer.validated_data}")
        
    # Проверяем создание
    if serializer.is_valid():
        subscription = serializer.save()
        print(f"  ✅ Подписка создана: ID {subscription.id}")
    else:
        print("  ❌ Ошибка валидации")
        
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
