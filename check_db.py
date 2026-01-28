import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

print("=== Проверка базы данных ===\n")

# Проверяем таблицы
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"1. Таблицы в базе данных ({len(tables)}):")
    for table in sorted(tables):
        print(f"   - {table[0]}")

# Проверяем, можем ли создать пользователя
print("\n2. Тест создания пользователя:")
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

print("\n3. Проверка количества записей:")
try:
    print(f"   - Пользователей: {User.objects.count()}")
    from materials.models import Course, Lesson
    print(f"   - Курсов: {Course.objects.count()}")
    print(f"   - Уроков: {Lesson.objects.count()}")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

print("\n=== Проверка завершена ===")
