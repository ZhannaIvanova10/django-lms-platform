from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet для платежей с фильтрацией"""
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.AllowAny]
    
    # Задание 4: Настройка фильтрации
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    
    # Поля для фильтрации (упрощенный формат)
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    
    # Поля для сортировки по дате оплаты
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # По умолчанию сортировка по дате (новые сверху)
    
    def perform_create(self, serializer):
        """При создании платежа устанавливаем текущего пользователя"""
        serializer.save(user=self.request.user)
