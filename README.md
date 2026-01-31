# Django LMS Platform

## Описание
Система управления обучением (LMS) с REST API на Django REST Framework.

## Выполненные задания

### Задание 1 (Первая домашка):
- [x] Создан Django-проект с DRF
- [x] Кастомная модель пользователя с авторизацией по email
- [x] Модели курса и урока со связью ForeignKey
- [x] CRUD: ViewSet для курсов, Generic-классы для уроков
- [x] Сериализаторы для всех моделей

### Задание 2 (Вторая домашка):
- [x] Поле `lessons_count` через `SerializerMethodField()`
- [x] Модель платежей с полями: пользователь, дата, курс/урок, сумма, способ оплаты
- [x] Кастомная команда для загрузки тестовых данных
- [x] Отдельный сериализатор `LessonInCourseSerializer` для уроков в курсе
- [x] Фильтрация платежей: сортировка по дате, фильтры по курсу/уроку/способу оплаты
- [x] История платежей в профиле пользователя (доп. задание)

## Установка

### 1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd django-lms-platform
```

### 2. Настройте базу данных:
Создайте файл `.env` из шаблона:
```bash
cp .env.example .env
```

Настройте PostgreSQL в `.env` файле или используйте SQLite (см. инструкцию ниже).

### 3. Установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 4. Выполните миграции:
```bash
python manage.py migrate
```

### 5. Загрузите тестовые данные:
```bash
python manage.py load_test_data
```

### 6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

### 7. Запустите сервер:
```bash
python manage.py runserver
```

## API Endpoints

### Основные эндпоинты:
- `GET /api/courses/` - список курсов с уроками и количеством уроков
- `GET /api/lessons/` - список уроков
- `GET /api/payments/` - список платежей с фильтрацией
- `POST /api/register/` - регистрация пользователя
- `GET /api/profile/` - профиль пользователя с историей платежей

### Фильтрация платежей:
- `GET /api/payments/?paid_course=1` - платежи за курс id=1
- `GET /api/payments/?paid_lesson=1` - платежи за урок id=1
- `GET /api/payments/?payment_method=cash` - платежи наличными
- `GET /api/payments/?ordering=payment_date` - сортировка по возрастанию даты
- `GET /api/payments/?ordering=-payment_date` - сортировка по убыванию даты

## Использование SQLite (если PostgreSQL не установлен)
Замените в `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Структура проекта
```
django-lms-platform/
├── config/              # Настройки проекта
├── users/              # Приложение пользователей
├── materials/          # Приложение курсов и уроков
├── lms/               # Приложение платежей
├── .env.example       # Шаблон переменных окружения
├── requirements.txt   # Зависимости
└── manage.py          # Скрипт управления Django
```

## Технологии
- Django 6.0
- Django REST Framework 3.16
- PostgreSQL / SQLite
- Django Filter
- Django CORS Headers
