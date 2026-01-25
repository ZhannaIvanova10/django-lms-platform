from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from .permissions import IsModerator


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для пользователей"""
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от действия"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    def get_permissions(self):
        """Определяем права доступа в зависимости от действия"""
        if self.action == 'create':
            # Регистрация доступна всем
            self.permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Обновлять и удалять может только владелец профиля
            self.permission_classes = [IsAuthenticated]
        else:
            # Просматривать список и детали может любой аутентифицированный пользователь
            self.permission_classes = [IsAuthenticated]
        
        return [permission() for permission in self.permission_classes]
    
    def perform_create(self, serializer):
        """При создании пользователя устанавливаем пароль"""
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
    
    def perform_update(self, serializer):
        """При обновлении пользователя проверяем пароль"""
        user = serializer.save()
        if 'password' in serializer.validated_data:
            user.set_password(serializer.validated_data['password'])
            user.save()
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """API для профиля пользователя (дополнительное задание)"""
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Возвращает текущего пользователя"""
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    """Кастомный view для получения JWT токена"""
    permission_classes = [AllowAny]
