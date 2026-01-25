import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

print("=== СУЩЕСТВУЮЩИЕ ПОЛЬЗОВАТЕЛИ ===")
for user in User.objects.all():
    print(f"ID: {user.id}, Email: {user.email}, Username: {user.username}, Is Staff: {user.is_staff}, Is Superuser: {user.is_superuser}")
