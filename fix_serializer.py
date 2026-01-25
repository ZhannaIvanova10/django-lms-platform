import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Читаем текущий файл
with open('materials/serializers.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем поля в SubscriptionSerializer
import re

# Находим класс SubscriptionSerializer
pattern = r'class SubscriptionSerializer\(serializers\.ModelSerializer\):(.*?)def create'
match = re.search(pattern, content, re.DOTALL)

if match:
    print("Найден SubscriptionSerializer")
    
    # Ищем мета-класс внутри
    meta_pattern = r'class Meta:(.*?)(?=\n\n|\Z)'
    meta_match = re.search(meta_pattern, match.group(1), re.DOTALL)
    
    if meta_match:
        print("Текущий Meta класс:")
        print(meta_match.group(1))
        
        # Заменяем поля на правильные
        new_content = content.replace(
            "        fields = ['id', 'user', 'course', 'is_active', 'created_at']",
            "        fields = ['id', 'user', 'course', 'is_active']"
        ).replace(
            "        read_only_fields = ['user', 'created_at']",
            "        read_only_fields = ['user']"
        )
        
        with open('materials/serializers.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("\n✅ Файл исправлен!")
    else:
        print("Meta класс не найден")
else:
    print("SubscriptionSerializer не найден")
