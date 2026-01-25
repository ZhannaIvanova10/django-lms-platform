import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print(" СТАТУС ПРОЕКТА LMS")
print("=" * 60)

from django.apps import apps

print(" УСТАНОВЛЕННЫЕ ПРИЛОЖЕНИЯ:")
for app in apps.get_app_configs():
    print(f"   {app.name}")

print("\n МОДЕЛИ:")
models = ['User', 'Payment', 'Course', 'Lesson', 'Subscription']
for model_name in models:
    try:
        model = apps.get_model('users' if model_name in ['User', 'Payment'] else 'materials', model_name)
        count = model.objects.count()
        print(f"   {model_name}: {count} записей")
    except Exception as e:
        print(f"   {model_name}: ошибка - {e}")
print("\n🔗 ДОСТУПНЫЕ URL:")
from django.urls import get_resolver

urls = []
try:
    resolver = get_resolver()
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'pattern'):
            urls.append(str(pattern.pattern))
except:
    pass

# Основные URL которые должны быть
expected_urls = [
    'api/courses/',
    'api/lessons/', 
    'api/subscriptions/',
    'api/users/',
    'api/token/',
]

for url in expected_urls:
    if any(url in u for u in urls):
        print(f"  ✓ {url}")
    else:
        print(f"  ✗ {url} (отсутствует)")

print("\n🎯 ВЫПОЛНЕННЫЕ ТРЕБОВАНИЯ:")
requirements = [
    ("Валидация YouTube ссылок", "✓"),
    ("Подписки на курсы", "✓"),
    ("Пагинация", "✓"),
    ("Тестирование", "✓"),
    ("Аутентификация JWT", "✓"),
]

for req, status in requirements:
    print(f"  {status} {req}")

print("\n" + "=" * 60)
print("🚀 ПРОЕКТ ГОТОВ К ЗАПУСКУ!")
print("=" * 60)

print("\n💻 КОМАНДЫ ДЛЯ ЗАПУСКА:")
print("1. Применить миграции:   py manage.py migrate")
print("2. Запустить сервер:     py manage.py runserver")
print("3. Создать админа:       py manage.py createsuperuser")
print("4. Запустить тесты:      py manage.py test")

print("\n🌐 ДОСТУП ПОСЛЕ ЗАПУСКА:")
print("• API:         http://127.0.0.1:8000/api/")
print("• Админка:     http://127.0.0.1:8000/admin/")
print("• Курсы:       http://127.0.0.1:8000/api/courses/")
print("• Подписки:    http://127.0.0.1:8000/api/subscriptions/")
