import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.conf import settings

print("=== Проверка настроек ===")
print(f"1. DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
print(f"2. DATABASE NAME: {settings.DATABASES['default']['NAME']}")
print(f"3. AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")
print(f"4. INSTALLED_APPS: {len(settings.INSTALLED_APPS)} приложений")

# Проверяем подключение к базе данных
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("5. ✅ Подключение к базе данных: OK")
except Exception as e:
    print(f"5. ❌ Подключение к базе данных: {e}")

print("\n=== Проверка завершена ===")
