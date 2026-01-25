import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User, Payment
from materials.models import Course, Lesson

print("=== ФИНАЛЬНАЯ ПРОВЕРКА БАЗЫ ДАННЫХ ===")
print("")
print("📊 СТАТИСТИКА:")
print(f"👥 Пользователи: {User.objects.count()}")
print(f"📚 Курсы: {Course.objects.count()}")
print(f"📝 Уроки: {Lesson.objects.count()}")
print(f"💰 Платежи: {Payment.objects.count()}")
print("")

if Payment.objects.count() > 0:
    print("📋 ПОСЛЕДНИЕ ПЛАТЕЖИ:")
    for payment in Payment.objects.all().order_by('-payment_date')[:5]:
        course_name = payment.course.title if payment.course else "Нет курса"
        lesson_name = payment.lesson.title if payment.lesson else "Нет урока"
        print(f"  - {payment.payment_date.strftime('%Y-%m-%d')}: {payment.amount:.2f} руб. ({payment.payment_method})")
        print(f"    Курс: {course_name}, Урок: {lesson_name}")
        print("")
# Проверим суперпользователей
superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    print("👑 СУПЕРПОЛЬЗОВАТЕЛИ:")
    for user in superusers:
        print(f"  - {user.email} ({user.username})")
else:
    print("⚠️  Суперпользователи не найдены")
