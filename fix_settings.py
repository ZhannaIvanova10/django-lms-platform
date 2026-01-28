import re

with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Найдем и исправим проблемную секцию
# Ищем настройки для тестов
pattern = r"# Test database settings\nif 'test' in sys\.argv or 'test_coverage' in sys\.argv:\s+DATABASES = \{"
match = re.search(pattern, content, re.DOTALL)

if match:
    print("Найдены настройки тестов, исправляем...")
    # Просто удалим проблемную секцию и создадим новую
    new_test_settings = '''
# Test database settings - use SQLite for tests
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    
    # Speed up tests
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
'''
    # Удаляем старую секцию и добавляем новую
    content = re.sub(r"# Test database settings.*?(?=\n\n|\Z)", new_test_settings, content, flags=re.DOTALL)
    
    with open('config/settings.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Настройки тестов исправлены")
else:
    print("Настройки тестов не найдены, добавляем...")
    # Добавляем в конец файла
    new_test_settings = '''

# Test database settings - use SQLite for tests
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    
    # Speed up tests
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
'''
    with open('config/settings.py', 'a', encoding='utf-8') as f:
        f.write(new_test_settings)
    print("✅ Настройки тестов добавлены")
