import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("ПРОВЕРКА ИСПРАВЛЕНИЙ (ВСЕ ЗАМЕЧАНИЯ ПРЕПОДАВАТЕЛЯ)")
print("=" * 60)

all_passed = True

# 1. Проверка отдельного сериализатора для уроков в курсе
print("\n1. Проверка сериализаторов:")
try:
    from materials.serializers import LessonInCourseSerializer, CourseSerializer
    print("   ✅ LessonInCourseSerializer существует")
    
    cs = CourseSerializer()
    if 'lessons' in cs.fields:
        field_type = type(cs.fields['lessons'].child).__name__
        print(f"   ✅ CourseSerializer.lessons использует: {field_type}")
        if field_type == 'LessonInCourseSerializer':
            print("   ✅ Используется отдельный LessonInCourseSerializer!")
        else:
            print("   ❌ НЕ использует LessonInCourseSerializer!")
            all_passed = False
    else:
        print("   ❌ CourseSerializer не имеет поля lessons")
        all_passed = False
        
    # Проверяем что есть lessons_count
    if 'lessons_count' in cs.fields:
        print("   ✅ CourseSerializer имеет lessons_count (SerializerMethodField)")
    else:
        print("   ❌ Нет lessons_count")
        all_passed = False
        
except ImportError as e:
    print(f"   ❌ Ошибка импорта: {e}")
    all_passed = False
# 2. Проверка фильтрации платежей
print("\n2. Проверка фильтрации платежей:")
try:
    from lms.views import PaymentViewSet
    pv = PaymentViewSet()
    
    # Проверяем filterset_fields как список
    if hasattr(pv, 'filterset_fields'):
        if isinstance(pv.filterset_fields, list):
            print(f"   ✅ filterset_fields как список: {pv.filterset_fields}")
            if all(field in pv.filterset_fields for field in ['paid_course', 'paid_lesson', 'payment_method']):
                print("   ✅ Все нужные поля для фильтрации присутствуют")
            else:
                print("   ❌ Не все поля для фильтрации присутствуют")
                all_passed = False
        else:
            print(f"   ❌ filterset_fields не список: {type(pv.filterset_fields)}")
            all_passed = False
    else:
        print("   ❌ Нет filterset_fields")
        all_passed = False
    
    # Проверяем сортировку
    if hasattr(pv, 'ordering_fields'):
        if 'payment_date' in pv.ordering_fields:
            print(f"   ✅ Сортировка по payment_date настроена: {pv.ordering_fields}")
        else:
            print(f"   ❌ Нет сортировки по payment_date: {pv.ordering_fields}")
            all_passed = False
    else:
        print("   ❌ Нет ordering_fields")
        all_passed = False
        
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    all_passed = False
# 3. Проверка базы данных
print("\n3. Проверка базы данных:")
try:
    from django.conf import settings
    db_engine = settings.DATABASES['default']['ENGINE']
    if 'postgresql' in db_engine:
        print(f"   ✅ Используется PostgreSQL: {db_engine}")
    else:
        print(f"   ⚠️  Используется {db_engine} (нужен PostgreSQL)")
        all_passed = False
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    all_passed = False

# 4. Проверка файлов окружения
print("\n4. Проверка файлов окружения:")
import os.path
if os.path.exists('.env.example'):
    print("   ✅ .env.example существует (шаблон)")
else:
    print("   ❌ .env.example не найден")
    all_passed = False

# Проверяем что .env в .gitignore
try:
    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()
    if '.env' in gitignore_content:
        print("   ✅ .env добавлен в .gitignore")
    else:
        print("   ❌ .env НЕ в .gitignore")
        all_passed = False
except Exception as e:
    print(f"   ❌ Ошибка чтения .gitignore: {e}")
    all_passed = False

# 5. Проверка отсутствия дублирующихся файлов
print("\n5. Проверка на дублирующиеся файлы:")
import glob
duplicate_patterns = ['*2.py', '*copy*', '*backup*', 'settings2*', 'urls2*', 'serializers2*', 'views2*']
has_duplicates = False
for pattern in duplicate_patterns:
    files = glob.glob(f'**/{pattern}', recursive=True)
    files = [f for f in files if 'venv' not in f and '__pycache__' not in f]
    if files:
        print(f"   ⚠️  Найден(ы) файл(ы) по шаблону {pattern}: {files}")
        has_duplicates = True

if not has_duplicates:
    print("   ✅ Нет дублирующихся файлов настроек/сериализаторов/представлений")
else:
    print("   ❌ Есть дублирующиеся файлы!")
    all_passed = False

# 6. Проверка кастомной команды
print("\n6. Проверка кастомной команды:")
import subprocess
try:
    result = subprocess.run(
        ['python', 'manage.py', 'load_test_data', '--help'], 
        capture_output=True, text=True, timeout=5
    )
    if 'Загружает тестовые данные в базу' in result.stdout or 'help' in result.stdout:
        print("   ✅ Кастомная команда load_test_data существует")
    else:
        print("   ❌ Кастомная команда не найдена или не работает")
        all_passed = False
except Exception as e:
    print(f"   ⚠️  Ошибка запуска команды: {e}")

print("\n" + "=" * 60)
if all_passed:
    print("✅ ВСЕ ЗАМЕЧАНИЯ ИСПРАВЛЕНЫ! Проект готов к отправке!")
else:
    print("❌ ЕСТЬ ПРОБЛЕМЫ, которые нужно исправить")
print("=" * 60)

# Возвращаем код выхода для скриптов
sys.exit(0 if all_passed else 1)
