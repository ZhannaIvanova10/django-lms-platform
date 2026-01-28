import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print("Проверка импортов...")

# Проверяем основные импорты
modules_to_check = [
    ('materials.models', ['Course', 'Lesson']),
    ('materials.serializers', ['CourseSerializer', 'LessonSerializer']),
    ('materials.views', ['CourseViewSet', 'LessonViewSet']),
    ('users.models', ['User', 'Subscription']),
    ('users.serializers', ['UserSerializer', 'SubscriptionSerializer']),
    ('users.views', ['UserViewSet', 'SubscriptionView']),
]

for module_name, classes in modules_to_check:
    try:
        module = __import__(module_name, fromlist=classes)
        print(f"✅ {module_name}")
        for class_name in classes:
            if hasattr(module, class_name):
                print(f"   - {class_name}: OK")
            else:
                print(f"   - {class_name}: NOT FOUND")
    except Exception as e:
        print(f"❌ {module_name}: {e}")

print("\nПроверка Django настройки...")
try:
    import django
    django.setup()
    print("✅ Django настроен")
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    print(f"✅ User модель: {User}")
    
    print("\nПроверка URL...")
    from django.urls import get_resolver
    resolver = get_resolver()
    print(f"✅ URL резолвер загружен")
    
except Exception as e:
    print(f"❌ Ошибка Django: {e}")
    import traceback
    traceback.print_exc()
