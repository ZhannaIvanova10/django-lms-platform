import os

# Читаем текущий файл
with open('materials/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Найдем строки импорта
for i, line in enumerate(lines):
    if 'from .serializers import' in line or 'from .serializers import CourseSerializer, LessonSerializer' in line:
        print(f"Найдена строка импорта на строке {i+1}: {line.strip()}")
        
        # Добавим SubscriptionSerializer в импорт
        if 'SubscriptionSerializer' not in line:
            # Проверяем, есть ли уже импорт с другими сериализаторами
            if 'CourseSerializer, LessonSerializer' in line:
                lines[i] = line.replace(
                    'CourseSerializer, LessonSerializer',
                    'CourseSerializer, LessonSerializer, SubscriptionSerializer'
                )
                print(f"Добавлен SubscriptionSerializer в существующий импорт")
            elif 'from .serializers import' in line:
                # Добавляем в конец импорта
                lines[i] = line.rstrip() + ', SubscriptionSerializer\n'
                print(f"Добавлен SubscriptionSerializer")
        break
# Записываем обратно
with open('materials/views.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Импорт исправлен!")
