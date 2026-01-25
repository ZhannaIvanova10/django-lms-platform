from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока"""
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link', 'course', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса (Задание 1 и 3)"""
    
    # ЗАДАНИЕ 1: Поле с количеством уроков через SerializerMethodField
    lessons_count = serializers.SerializerMethodField()
    
    # ЗАДАНИЕ 3: Вложенные уроки через связанный сериализатор
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'owner', 'lessons', 'lessons_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'lessons', 'lessons_count']
    
    # ЗАДАНИЕ 1: Метод для получения количества уроков
    def get_lessons_count(self, obj):
        """Получение количества уроков в курсе"""
        return obj.lessons.count()
