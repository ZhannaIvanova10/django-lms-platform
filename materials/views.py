from rest_framework import viewsets, generics, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

# ========== КУРСЫ (ViewSet) ==========
class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курсов - используем ViewSets как требуется в задании"""
    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

# ========== УРОКИ (Generic классы) ==========
class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Список уроков и создание - используем Generic классы"""
    
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Детали, обновление и удаление урока - используем Generic классы"""
    
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]
