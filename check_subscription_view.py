import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🔍 ПРОВЕРКА SubscriptionAPIView:")

try:
    from materials.views import SubscriptionAPIView
    print("✅ SubscriptionAPIView импортирован успешно")
    
    # Проверяем атрибуты класса
    print(f"\n📋 Атрибуты класса:")
    print(f"   serializer_class: {SubscriptionAPIView.serializer_class}")
    print(f"   permission_classes: {SubscriptionAPIView.permission_classes}")
    
    if hasattr(SubscriptionAPIView, 'pagination_class'):
        print(f"   pagination_class: {SubscriptionAPIView.pagination_class}")
    # Проверяем методы
    print(f"\n📋 Методы класса:")
    methods = [m for m in dir(SubscriptionAPIView) 
               if not m.startswith('_') and callable(getattr(SubscriptionAPIView, m))]
    for method in sorted(methods):
        print(f"   - {method}")
    
    # Тестируем POST метод
    print(f"\n🧪 Тест POST метода:")
    
    from users.models import User
    from materials.models import Course
    from rest_framework.test import APIRequestFactory
    
    # Создаем тестовые данные
    user = User.objects.create_user(
        email='viewtest@example.com',
        password='test123'
    )
    course = Course.objects.create(
        title='View Test Course',
        description='Test',
        owner=user
    )
    print(f"   Пользователь: {user.email}")
    print(f"   Курс: {course.title} (ID: {course.id})")
    
    # Проверяем логику POST метода
    if hasattr(SubscriptionAPIView, 'post'):
        print(f"   ✅ Метод post() существует")
        
        # Создаем mock request с course_id
        factory = APIRequestFactory()
        request = factory.post('/api/subscriptions/', 
                             {'course_id': course.id}, 
                             format='json')
        request.user = user
        
        # Создаем экземпляр view
        view = SubscriptionAPIView()
        view.request = request
        view.format_kwarg = None
        
        # Проверяем get_queryset
        queryset = view.get_queryset()
        print(f"   ✅ get_queryset() возвращает: {queryset.model.__name__}")
        
        # Проверяем сериализатор
        serializer = view.get_serializer(data=request.data)
        print(f"   ✅ Сериализатор создан: {serializer.__class__.__name__}")
        
    else:
        print(f"   ❌ Метод post() не найден в SubscriptionAPIView")

    # Проверяем URL
    from django.urls import reverse
    try:
        url = reverse('subscriptions')
        print(f"\n🔗 URL подписок: {url}")
    except:
        print(f"\n❌ Не удалось получить URL для 'subscriptions'")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
