import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🔍 ПРОВЕРКА ИСПРАВЛЕННОГО SubscriptionSerializer:")

try:
    from materials.serializers import SubscriptionSerializer
    print("✅ SubscriptionSerializer импортирован успешно")
    
    # Проверяем поля
    serializer = SubscriptionSerializer()
    fields = list(serializer.fields.keys())
    print(f"✅ Поля сериализатора: {fields}")
    
    # Проверяем модель
    print(f"✅ Модель: {serializer.Meta.model.__name__}")
    print(f"✅ Read-only поля: {serializer.Meta.read_only_fields}")
    print(f"✅ Все поля: {serializer.Meta.fields}")
    
    # Тестируем создание
    from users.models import User
    from materials.models import Course
    
    user = User.objects.create_user(
        email='serializer_test@example.com',
        password='test123'
    )
    course = Course.objects.create(
        title='Serializer Test Course',
        description='Test',
        owner=user
    )
    print(f"\n🧪 Тест создания подписки:")
    print(f"   Пользователь: {user.email}")
    print(f"   Курс: {course.title}")
    
    # Создаем mock request
    from rest_framework.test import APIRequestFactory
    factory = APIRequestFactory()
    request = factory.post('/')
    request.user = user
    
    # Тестируем сериализатор
    data = {'course': course.id}
    serializer = SubscriptionSerializer(
        data=data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        print(f"   ✅ Данные валидны")
        print(f"   ✅ Валидированные данные: {serializer.validated_data}")
        
        # Пробуем сохранить
        subscription = serializer.save()
        print(f"   ✅ Подписка создана: ID {subscription.id}")
        print(f"   ✅ Пользователь: {subscription.user.email}")
        print(f"   ✅ Курс: {subscription.course.title}")
        print(f"   ✅ Активна: {subscription.is_active}")
    else:
        print(f"   ❌ Ошибки валидации: {serializer.errors}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
