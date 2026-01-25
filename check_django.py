import os
import sys
import django
from pathlib import Path

# Добавляем путь к проекту
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    from django.conf import settings
    
    print("=== ПРОВЕРКА НАСТРОЕК ===")
    print(f"Django version: {django.get_version()}")
    print(f"\nINSTALLED_APPS:")
    for app in settings.INSTALLED_APPS:
        print(f"  - {app}")
    
    # Проверим наличие django_filters
    if 'django_filters' in settings.INSTALLED_APPS:
        print(f"\n✅ django_filters найден в INSTALLED_APPS")
    else:
        print(f"\n❌ django_filters НЕ найден в INSTALLED_APPS")
        
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()
