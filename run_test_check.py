import os
import sys

# Устанавливаем режим тестирования
sys.argv.append('test')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    import django
    django.setup()
    print("✅ Django успешно настроен")
    
    from django.test import TestCase
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    class QuickTest(TestCase):
        def test_basic(self):
            user = User.objects.create_user(
                email='test@example.com',
                password='password123'
            )
            self.assertEqual(user.email, 'test@example.com')
            print("✅ Базовый тест прошел")
    
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(QuickTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.failures or result.errors:
        print(f"❌ Есть ошибки: {len(result.failures)} failures, {len(result.errors)} errors")
    else:
        print("✅ Все тесты прошли успешно")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
