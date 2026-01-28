from rest_framework import viewsets, generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from .models import Subscription
from .serializers import UserSerializer, SubscriptionSerializer
from materials.models import Course

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubscriptionView(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        if not course_id:
            return Response(
                {'error': 'Поле course_id обязательно'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {'error': 'Курс не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Проверяем, существует ли уже подписка
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            course=course
        )
        
        if created:
            serializer = self.get_serializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Если подписка уже существует - удаляем ее (переключение)
            subscription.delete()
            return Response(
                {'detail': 'Подписка удалена'},
                status=status.HTTP_200_OK
            )
