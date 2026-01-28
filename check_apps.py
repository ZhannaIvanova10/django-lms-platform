import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.apps import apps

print("Установленные приложения:")
for app in apps.get_app_configs():
    print(f"  - {app.name}")
    
print("\nМодели:")
for model in apps.get_models():
    print(f"  - {model._meta.app_label}.{model.__name__}")
