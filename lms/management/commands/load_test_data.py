from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from lms.models import Payment
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Загружает тестовые данные в базу'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Загрузка тестовых данных...'))
        
        # 1. Создаем пользователей
        admin, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Админ',
                'last_name': 'Админов',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Создан администратор: {admin.email}'))
        
        user1, created = User.objects.get_or_create(
            email='user1@example.com',
            defaults={
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'phone': '+79991234567',
                'city': 'Москва'
            }
        )
        if created:
            user1.set_password('user123')
            user1.save()
            self.stdout.write(self.style.SUCCESS(f'Создан пользователь: {user1.email}'))
        
        user2, created = User.objects.get_or_create(
            email='user2@example.com',
            defaults={
                'first_name': 'Мария',
                'last_name': 'Петрова',
                'phone': '+79997654321',
                'city': 'Санкт-Петербург'
            }
        )
        if created:
            user2.set_password('user123')
            user2.save()
            self.stdout.write(self.style.SUCCESS(f'Создан пользователь: {user2.email}'))
        # 2. Создаем курсы
        courses_data = [
            {
                'title': 'Python для начинающих',
                'description': 'Изучите основы Python с нуля'
            },
            {
                'title': 'Django разработка',
                'description': 'Создание веб-приложений на Django'
            },
            {
                'title': 'JavaScript и React',
                'description': 'Современный фронтенд разработка'
            }
        ]
        
        courses = []
        for data in courses_data:
            course, created = Course.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'owner': admin
                }
            )
            courses.append(course)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан курс: {course.title}'))
        
        # 3. Создаем уроки
        lessons = []
        lesson_counter = 1
        
        for course in courses:
            for i in range(1, 4):  # 3 урока на курс
                lesson, created = Lesson.objects.get_or_create(
                    title=f'Урок {i}: {course.title}',
                    defaults={
                        'description': f'Описание урока {i} для курса "{course.title}"',
                        'video_url': f'https://example.com/video/{lesson_counter}',
                        'course': course,
                        'owner': admin
                    }
                )
                lessons.append(lesson)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Создан урок: {lesson.title}'))
                lesson_counter += 1
        # 4. Создаем платежи
        payments_data = [
            # Платежи за курсы
            {'user': user1, 'course': courses[0], 'lesson': None, 'amount': 10000, 'method': 'transfer'},
            {'user': user2, 'course': courses[1], 'lesson': None, 'amount': 15000, 'method': 'transfer'},
            {'user': user1, 'course': courses[2], 'lesson': None, 'amount': 12000, 'method': 'cash'},
            
            # Платежи за уроки
            {'user': user1, 'course': None, 'lesson': lessons[0], 'amount': 2000, 'method': 'cash'},
            {'user': user2, 'course': None, 'lesson': lessons[3], 'amount': 2500, 'method': 'transfer'},
            {'user': admin, 'course': None, 'lesson': lessons[6], 'amount': 3000, 'method': 'transfer'},
        ]
        
        # Добавляем разные даты для тестирования сортировки
        for i, data in enumerate(payments_data):
            payment_date = datetime.now() - timedelta(days=i*2)  # Разные даты
            payment, created = Payment.objects.get_or_create(
                user=data['user'],
                paid_course=data['course'],
                paid_lesson=data['lesson'],
                defaults={
                    'amount': data['amount'],
                    'payment_method': data['method'],
                    'payment_date': payment_date
                }
            )
            if created:
                item = payment.paid_course or payment.paid_lesson
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Создан платеж: {payment.user.email} -> {item.title} '
                        f'({payment.amount} руб., {payment.payment_method})'
                    )
                )
        
        # Выводим статистику
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('СТАТИСТИКА:'))
        self.stdout.write(self.style.SUCCESS(f'👤 Пользователей: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📚 Курсов: {Course.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📖 Уроков: {Lesson.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'💰 Платежей: {Payment.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS('✅ Тестовые данные успешно загружены!'))
