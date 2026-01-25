from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserCreateSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для пользователей (CRUD)"""
    
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
