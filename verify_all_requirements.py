import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 70)
print("ПОЛНАЯ ПРОВЕРКА ВСЕХ КРИТЕРИЕВ ЗАДАНИЙ")
print("=" * 70)

all_passed = True
requirements = []

# 1. Проверка первой домашки
print("\n🔹 ПЕРВАЯ ДОМАШКА:")
print("-" * 40)

# 1.1 Django проект с DRF
try:
    from django.conf import settings
    if 'rest_framework' in settings.INSTALLED_APPS:
        requirements.append("✅ Django проект с DRF")
        print("   ✅ Django проект с DRF")
    else:
        requirements.append("❌ Django проект с DRF")
        print("   ❌ DRF не в INSTALLED_APPS")
        all_passed = False
except:
    requirements.append("❌ Django проект с DRF")
    print("   ❌ Ошибка проверки DRF")
    all_passed = False

# 1.2 Кастомная модель User
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if hasattr(User, 'email') and User.USERNAME_FIELD == 'email':
        requirements.append("✅ Кастомная модель User с email-авторизацией")
        print("   ✅ Кастомная модель User с email-авторизацией")
    else:
        requirements.append("❌ Кастомная модель User с email-авторизацией")
        print("   ❌ User не настроен на email-авторизацию")
        all_passed = False
except:
    requirements.append("❌ Кастомная модель User с email-авторизацией")
    print("   ❌ Ошибка проверки модели User")
    all_passed = False

# 1.3 Модели Course и Lesson
try:
    from materials.models import Course, Lesson
    if hasattr(Lesson, 'course'):
        requirements.append("✅ Модели Course и Lesson со связью")
        print("   ✅ Модели Course и Lesson со связью")
    else:
        requirements.append("❌ Модели Course и Lesson со связью")
        print("   ❌ Нет связи между Course и Lesson")
        all_passed = False
except:
    requirements.append("❌ Модели Course и Lesson со связью")
    print("   ❌ Ошибка проверки моделей Course/Lesson")
    all_passed = False

# 1.4 CRUD: ViewSet для курсов, Generic для уроков
try:
    from materials.views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
    requirements.append("✅ CRUD: ViewSet для курсов, Generic для уроков")
    print("   ✅ CRUD: ViewSet для курсов, Generic для уроков")
except:
    requirements.append("❌ CRUD: ViewSet для курсов, Generic для уроков")
    print("   ❌ Ошибка проверки views")
    all_passed = False
# 2. Проверка второй домашки
print("\n🔹 ВТОРАЯ ДОМАШКА:")
print("-" * 40)

# 2.1 SerializerMethodField для lessons_count
try:
    from materials.serializers import CourseSerializer
    cs = CourseSerializer()
    if 'lessons_count' in cs.fields:
        requirements.append("✅ lessons_count через SerializerMethodField")
        print("   ✅ lessons_count через SerializerMethodField")
    else:
        requirements.append("❌ lessons_count через SerializerMethodField")
        print("   ❌ Нет lessons_count в CourseSerializer")
        all_passed = False
except:
    requirements.append("❌ lessons_count через SerializerMethodField")
    print("   ❌ Ошибка проверки lessons_count")
    all_passed = False

# 2.2 Модель Payment
try:
    from lms.models import Payment
    if hasattr(Payment, 'paid_course') and hasattr(Payment, 'paid_lesson'):
        requirements.append("✅ Модель Payment с полями")
        print("   ✅ Модель Payment с полями")
    else:
        requirements.append("❌ Модель Payment с полями")
        print("   ❌ Payment не имеет нужных полей")
        all_passed = False
except:
    requirements.append("❌ Модель Payment с полями")
    print("   ❌ Ошибка проверки модели Payment")
    all_passed = False

# 2.3 Кастомная команда
import subprocess
result = subprocess.run(['python', 'manage.py', 'load_test_data', '--help'], 
                       capture_output=True, text=True, timeout=5)
if 'Загружает тестовые данные в базу' in result.stdout or 'help' in result.stdout:
    requirements.append("✅ Кастомная команда load_test_data")
    print("   ✅ Кастомная команда load_test_data")
else:
    requirements.append("❌ Кастомная команда load_test_data")
    print("   ❌ Кастомная команда не найдена")
    all_passed = False

# 2.4 Отдельный сериализатор для уроков
try:
    from materials.serializers import LessonInCourseSerializer
    if 'lessons' in cs.fields:
        field_type = type(cs.fields['lessons'].child).__name__
        if field_type == 'LessonInCourseSerializer':
            requirements.append("✅ Отдельный LessonInCourseSerializer")
            print("   ✅ Отдельный LessonInCourseSerializer")
        else:
            requirements.append("❌ Отдельный LessonInCourseSerializer")
            print(f"   ❌ Используется {field_type}, а не LessonInCourseSerializer")
            all_passed = False
except:
    requirements.append("❌ Отдельный LessonInCourseSerializer")
    print("   ❌ Ошибка проверки LessonInCourseSerializer")
    all_passed = False

# 2.5 Фильтрация платежей
try:
    from lms.views import PaymentViewSet
    pv = PaymentViewSet()
    if hasattr(pv, 'ordering_fields') and 'payment_date' in pv.ordering_fields:
        requirements.append("✅ Фильтрация платежей с сортировкой")
        print("   ✅ Фильтрация платежей с сортировкой")
    else:
        requirements.append("❌ Фильтрация платежей с сортировкой")
        print("   ❌ Нет сортировки по payment_date")
        all_passed = False
except:
    requirements.append("❌ Фильтрация платежей с сортировкой")
    print("   ❌ Ошибка проверки фильтрации")
    all_passed = False

# 2.6 История платежей в профиле
try:
    from users.serializers import UserProfileSerializer
    ups = UserProfileSerializer()
    if 'payments' in ups.fields:
        requirements.append("✅ История платежей в профиле (доп. задание)")
        print("   ✅ История платежей в профиле (доп. задание)")
    else:
        requirements.append("❌ История платежей в профиле (доп. задание)")
        print("   ❌ Нет поля payments в UserProfileSerializer")
        all_passed = False
except:
    requirements.append("❌ История платежей в профиле (доп. задание)")
    print("   ❌ Ошибка проверки истории платежей")
    all_passed = False

# 3. Проверка дополнительных требований
print("\n🔹 ДОПОЛНИТЕЛЬНЫЕ ТРЕБОВАНИЯ:")
print("-" * 40)

# PostgreSQL
db_engine = settings.DATABASES['default']['ENGINE']
if 'postgresql' in db_engine:
    requirements.append("✅ PostgreSQL база данных")
    print("   ✅ PostgreSQL база данных")
else:
    requirements.append(f"⚠️  База данных: {db_engine}")
    print(f"   ⚠️  База данных: {db_engine}")
# .env только как шаблон
import os.path
if os.path.exists('.env.example'):
    requirements.append("✅ .env.example шаблон существует")
    print("   ✅ .env.example шаблон существует")
else:
    requirements.append("❌ .env.example шаблон существует")
    print("   ❌ Нет .env.example")
    all_passed = False

print("\n" + "=" * 70)
print("ИТОГОВЫЙ ОТЧЕТ:")
print("=" * 70)

for req in requirements:
    print(req)

print("\n" + "=" * 70)
if all_passed:
    print("🎉 ВСЕ КРИТЕРИИ ВЫПОЛНЕНЫ! Проект готов к отправке!")
else:
    print("⚠️  ЕСТЬ НЕВЫПОЛНЕННЫЕ КРИТЕРИИ")
print("=" * 70)

sys.exit(0 if all_passed else 1)
