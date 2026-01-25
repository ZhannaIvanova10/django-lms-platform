import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from materials.models import Course, Subscription

print("📊 ТЕКУЩЕЕ СОСТОЯНИЕ БАЗЫ ДАННЫХ:")
print(f"Пользователей: {User.objects.count()}")
print(f"Курсов: {Course.objects.count()}")
print(f"Подписок: {Subscription.objects.count()}")

if Subscription.objects.exists():
    print("\n📋 Список подписок:")
    for sub in Subscription.objects.all():
        print(f"  - {sub.user.email} -> {sub.course.title} (активна: {sub.is_active})")
else:
    print("\n❌ Подписок нет в базе данных")
# Проверяем сериализатор подписок
try:
    from materials.serializers import SubscriptionSerializer
    print("\n✅ Сериализатор SubscriptionSerializer загружен")
    
    # Проверяем поля сериализатора
    serializer = SubscriptionSerializer()
    print(f"Поля сериализатора: {list(serializer.fields.keys())}")
except ImportError as e:
    print(f"\n❌ Ошибка импорта: {e}")

# Проверяем URL подписок
from django.urls import reverse, resolve
try:
    print("\n🔗 Проверка URL подписок:")
    url = reverse('subscriptions')
    print(f"  URL: {url}")
    
    # Проверяем view
    match = resolve(url)
    print(f"  View: {match.func}")
    
    # Импортируем view чтобы проверить
    view_class = match.func.cls
    print(f"  View класс: {view_class}")
    
    # Проверяем методы
    print(f"  Методы разрешены: {view_class.http_method_names}")
    
except Exception as e:
    print(f"  ❌ Ошибка: {e}")
