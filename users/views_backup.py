from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import User, Payment
from .serializers import UserProfileSerializer, PaymentSerializer
from .filters import PaymentFilter


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # Подключаем фильтрацию и сортировку
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter

    # Настраиваем сортировку
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # По умолчанию сортировка по дате (новые сначала)
