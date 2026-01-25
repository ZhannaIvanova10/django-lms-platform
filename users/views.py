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
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer, UserWithPaymentsSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet для платежей с фильтрацией (Задание 4)"""
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    
    # ЗАДАНИЕ 4: Фильтры
    filterset_fields = {
        'course': ['exact'],
        'lesson': ['exact'],
        'payment_method': ['exact'],
    }
    
    # ЗАДАНИЕ 4: Сортировка
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']  # По умолчанию сортировка по дате (новые сначала)
    
    # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: Переопределяем get_serializer_class для User
    def get_serializer_class(self):
        if self.action == 'retrieve' and 'payments' in self.request.query_params.get('include', ''):
            return UserWithPaymentsSerializer
        return super().get_serializer_class()
