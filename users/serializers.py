from rest_framework import serializers
from .models import User
from lms.serializers import PaymentSerializer


class UserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор пользователя"""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar']


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя с платежами"""
    
    # Дополнительное задание: История платежей пользователя
    payments = PaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'phone', 'city', 'avatar', 'payments'
        ]
        read_only_fields = ['email']
