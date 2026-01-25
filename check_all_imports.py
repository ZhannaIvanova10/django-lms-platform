import os
import sys

# Добавим путь к проекту
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print("=== ПОЛНАЯ ПРОВЕРКА ИМПОРТОВ ===\n")

try:
    # 1. Django
    import django
    django.setup()
    print("1. ✅ Django загружен")
    
    # 2. Модели
    from users.models import User
    print("2. ✅ User модель")
    from materials.models import Course, Lesson
    print("3. ✅ Course и Lesson модели")
    
    # 3. Сериализаторы
    from users.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
    print("4. ✅ User сериализаторы")
    from materials.serializers import CourseSerializer, LessonSerializer
    print("5. ✅ Course и Lesson сериализаторы")
    
    # 4. Views
    from users.views import UserViewSet, UserProfileAPIView
    print("6. ✅ User views")
    from materials.views import CourseViewSet, LessonViewSet
    print("7. ✅ Course и Lesson views")
    # 5. Permissions
    from users.permissions import IsModerator, IsOwner, IsCourseOwner, IsLessonOwner
    print("8. ✅ Permissions")
    
    # 6. JWT
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    print("9. ✅ JWT views")
    
    print("\n🎉 ВСЕ ИМПОРТЫ УСПЕШНЫ!")
    
except ImportError as e:
    print(f"\n❌ ОШИБКА ИМПОРТА: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()
