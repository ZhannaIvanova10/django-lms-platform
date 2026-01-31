import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from lms.models import Payment

User = get_user_model()

print("=" * 50)
print("ПРОВЕРКА ДАННЫХ В БАЗЕ")
print("=" * 50)

print(f"👤 Пользователей: {User.objects.count()} (должно быть 3)")
print(f"📚 Курсов: {Course.objects.count()} (должно быть 3)")
print(f"📖 Уроков: {Lesson.objects.count()} (должно быть 9)")
print(f"💰 Платежей: {Payment.objects.count()} (должно быть 6)")

# Проверка связей
course = Course.objects.first()
if course:
    print(f"\n📊 Проверка курса '{course.title}':")
    print(f"   Уроков в курсе: {course.lessons.count()} (должно быть 3)")

# Проверка фильтрации
cash_payments = Payment.objects.filter(payment_method='cash').count()
print(f"\n💵 Платежей наличными: {cash_payments} (должно быть 2)")

course_payments = Payment.objects.filter(paid_course__isnull=False).count()
print(f"🎓 Платежей за курсы: {course_payments} (должно быть 3)")

lesson_payments = Payment.objects.filter(paid_lesson__isnull=False).count()
print(f"📝 Платежей за уроки: {lesson_payments} (должно быть 3)")

print("\n" + "=" * 50)
print("✅ Все проверки пройдены!" if all([
    User.objects.count() == 3,
    Course.objects.count() == 3,
    Lesson.objects.count() == 9,
    Payment.objects.count() == 6,
    cash_payments == 2,
    course_payments == 3,
    lesson_payments == 3
]) else "❌ Есть проблемы с данными")
print("=" * 50)
