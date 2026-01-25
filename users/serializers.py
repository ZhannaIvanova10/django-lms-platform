from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'city']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# ЗАДАНИЕ 4 и ДОПОЛНИТЕЛЬНОЕ: Сериализатор для платежей
class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""
    # Показываем информацию о пользователе
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    # Показываем информацию о курсе/уроке
    course_title = serializers.CharField(source='course.title', read_only=True, allow_null=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True, allow_null=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_email', 'course', 'course_title', 
            'lesson', 'lesson_title', 'payment_date', 'amount', 
            'payment_method'
        ]
        read_only_fields = ['id', 'payment_date']

# ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: Сериализатор для пользователя с платежами
class UserWithPaymentsSerializer(UserSerializer):
    """Сериализатор для пользователя с историей платежей"""
    
    payments = PaymentSerializer(many=True, read_only=True)
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['payments']
