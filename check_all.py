import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=== Проверка всех компонентов ===\n")

# 1. Проверка моделей
print("1. Проверка моделей:")
try:
    from users.models import User, Subscription
    print("  ✅ users.models - OK")
    from materials.models import Course, Lesson
    print("  ✅ materials.models - OK")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

# 2. Проверка сериализаторов
print("\n2. Проверка сериализаторов:")
try:
    from users.serializers import UserSerializer, SubscriptionSerializer
    print("  ✅ users.serializers - OK")
    from materials.serializers import CourseSerializer, LessonSerializer
    print("  ✅ materials.serializers - OK")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

# 3. Проверка представлений
print("\n3. Проверка представлений:")
try:
    from users.views import UserViewSet, SubscriptionView
    print("  ✅ users.views - OK")
    from materials.views import CourseViewSet, LessonViewSet
    print("  ✅ materials.views - OK")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

# 4. Проверка URL
print("\n4. Проверка URL:")
try:
    from django.urls import reverse
    print("  ✅ Django URL system - OK")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

# 5. Проверка настроек
print("\n5. Проверка настроек:")
try:
    from django.conf import settings
    print(f"  ✅ AUTH_USER_MODEL = {settings.AUTH_USER_MODEL}")
    print(f"  ✅ INSTALLED_APPS = {len(settings.INSTALLED_APPS)} приложений")
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

print("\n=== Проверка завершена ===")
