import re

with open('config/settings.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Найдем строки с ошибкой
for i, line in enumerate(lines):
    if 'if \'test\' in sys.argv or \'test_coverage\' in sys.argv:' in line:
        print(f"Найдена проблемная строка {i+1}: {line.strip()}")
        
        # Проверим отступы
        if not line.startswith('    '):
            print(f"Неправильные отступы в строке {i+1}")
            # Исправляем отступы
            lines[i] = '    ' + line.lstrip()
        
        # Проверим следующую строку
        if i+1 < len(lines):
            next_line = lines[i+1]
            if 'DATABASES = {' in next_line and not next_line.startswith('        '):
                print(f"Неправильные отступы в строке {i+2}")
                lines[i+1] = '        ' + next_line.lstrip()

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Исправлены отступы в settings.py")
