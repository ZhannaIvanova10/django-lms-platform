from rest_framework import serializers
from .models import Course, Lesson


class LessonInCourseSerializer(serializers.ModelSerializer):
    """Отдельный сериализатор для отображения уроков внутри курса"""
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video_url']


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков (используется в отдельных эндпоинтах)"""
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course']


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов с уроками"""
    
    # Задание 1: Количество уроков через SerializerMethodField
    lessons_count = serializers.SerializerMethodField()
    
    # Задание 3: Список уроков через ОТДЕЛЬНЫЙ связанный сериализатор
    lessons = LessonInCourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'preview', 'description',
            'lessons_count', 'lessons', 'owner', 'created_at'
        ]
        read_only_fields = ['owner', 'created_at']
    
    def get_lessons_count(self, obj):
        """Получение количества уроков в курсе"""
        return obj.lessons.count()
