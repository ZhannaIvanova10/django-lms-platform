from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'date_joined']
        read_only_fields = ['id', 'date_joined']
        
    def create(self, validated_data):
        """Создание пользователя с паролем"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'city']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
