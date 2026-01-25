from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsCourseOwner, IsLessonOwner


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'title']
    
    def get_permissions(self):
        """Определяем права доступа в зависимости от действия"""
        if self.action == 'create':
            # Создавать курс может только аутентифицированный пользователь и не модератор
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            # Обновлять курс может владелец или модератор
            self.permission_classes = [IsAuthenticated, IsCourseOwner | IsModerator]
        elif self.action == 'destroy':
            # Удалять курс может только владелец (не модератор)
            self.permission_classes = [IsAuthenticated, IsCourseOwner, ~IsModerator]
        else:
            # Просматривать список и детали может любой аутентифицированный пользователь
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
    
    def perform_create(self, serializer):
        """Автоматически назначаем владельца при создании курса"""
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet для уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'title']
    
    def get_permissions(self):
        """Определяем права доступа в зависимости от действия"""
        if self.action == 'create':
            # Создавать урок может только аутентифицированный пользователь и не модератор
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            # Обновлять урок может владелец или модератор
            self.permission_classes = [IsAuthenticated, IsLessonOwner | IsModerator]
        elif self.action == 'destroy':
            # Удалять урок может только владелец (не модератор)
            self.permission_classes = [IsAuthenticated, IsLessonOwner, ~IsModerator]
        else:
            # Просматривать список и детали может любой аутентифицированный пользователь
            self.permission_classes = [IsAuthenticated]
        
        return [permission() for permission in self.permission_classes]
    
    def perform_create(self, serializer):
        """Автоматически назначаем владельца при создании урока"""
        serializer.save(owner=self.request.user)
