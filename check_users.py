import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

print("=== СУЩЕСТВУЮЩИЕ ПОЛЬЗОВАТЕЛЬ ===")
for user in User.objects.all():
    print(f"ID: {user.id}, Email: {user.email}")
