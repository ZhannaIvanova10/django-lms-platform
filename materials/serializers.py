from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_url, validate_description


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


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'preview', 'owner',
            'created_at', 'updated_at', 'lessons_count',
            'lessons', 'is_subscribed'
        ]
        validators = [
            validate_description,
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
    
    def get_is_subscribed(self, obj):
        """
        Проверяем, подписан ли текущий пользователь на курс
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj,
                is_active=True
            ).exists()
        return False
    
    def validate(self, data):
        """
        Дополнительная валидация данных курса
        """
        # Проверяем описание
        description = data.get('description')
        if description:
            validate_description(description)
        
        return data

class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'is_active']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        """Автоматически устанавливаем текущего пользователя"""
        user = self.context['request'].user
        course = validated_data.get('course')
        
        # Проверяем, существует ли уже подписка
        subscription, created = Subscription.objects.get_or_create(
            user=user,
            course=course,
            defaults={'is_active': True}
        )
        
        if not created:
            # Если подписка уже существует, переключаем её активность
            subscription.is_active = not subscription.is_active
            subscription.save()
        
        return subscription
