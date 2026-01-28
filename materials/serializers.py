from rest_framework import serializers
from materials.models import Lesson, Course, Subscription
from materials.validators import validate_video_url, validate_description


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            validate_video_url,
            validate_description,
        ]

    def validate(self, data):
        """
        Дополнительная валидация данных урока
        """
        # Проверяем video_url
        video_url = data.get('video_url')
        if video_url:
            validate_video_url(video_url)
        # Проверяем описание
        description = data.get('description')
        if description:
            validate_description(description)
        return data


class LessonShortSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для отображения уроков в курсе"""

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video_url', 'order']
        read_only_fields = ['id']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(many=True, read_only=True, source='lessons')

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'owner',
                 'created_at', 'updated_at', 'lessons_count', 'lessons']
        read_only_fields = ['id', 'owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
