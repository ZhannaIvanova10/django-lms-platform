import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

print("=== Проверка базы данных SQLite ===\n")

# Проверяем подключение
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        print(f"1. Таблицы в базе данных ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
except Exception as e:
    print(f"1. ❌ Ошибка при проверке таблиц: {e}")

# Проверяем пользователей
print("\n2. Пользователи в системе:")
try:
    users = User.objects.all()
    if users.exists():
        for user in users:
            print(f"   - {user.email} (id: {user.id})")
    else:
        print("   - Нет пользователей")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

# Проверяем создание нового пользователя
print("\n3. Тест создания пользователя:")
try:
    user, created = User.objects.get_or_create(
        email='test@example.com',
        defaults={'first_name': 'Test', 'last_name': 'User'}
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f"   ✅ Создан пользователь: {user.email}")
    else:
        print(f"   ✅ Пользователь уже существует: {user.email}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

print("\n=== Проверка завершена ===")
