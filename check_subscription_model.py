import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from materials.models import Subscription
import inspect

print("🔍 ПОЛЯ МОДЕЛИ SUBSCRIPTION:")
print(f"Модель: {Subscription}")

# Получаем все поля модели
fields = Subscription._meta.fields
for field in fields:
    print(f"  - {field.name}: {field.__class__.__name__}")

# Проверяем есть ли created_at
field_names = [f.name for f in fields]
print(f"\n📋 Все поля: {field_names}")

# Проверяем Meta класс модели
print(f"\n📋 Метаданные модели:")
print(f"  db_table: {Subscription._meta.db_table}")
print(f"  verbose_name: {Subscription._meta.verbose_name}")
print(f"  verbose_name_plural: {Subscription._meta.verbose_name_plural}")
# Проверяем миграции
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute(f"PRAGMA table_info({Subscription._meta.db_table});")
    columns = cursor.fetchall()
    print(f"\n📊 СТОЛБЦЫ В БАЗЕ ДАННЫХ:")
    for col in columns:
        print(f"  - {col[1]}: {col[2]} (primary: {col[5]})")
