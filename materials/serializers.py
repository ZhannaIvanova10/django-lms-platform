from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока"""
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link', 'course', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""
    
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'owner', 'lessons', 'lessons_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'lessons', 'lessons_count']
