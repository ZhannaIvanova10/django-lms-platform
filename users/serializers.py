from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Subscription

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone']
        read_only_fields = fields

class SubscriptionSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True, required=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'course_id', 'created_at']
        read_only_fields = ['user', 'course', 'created_at']
