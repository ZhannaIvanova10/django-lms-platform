import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    payment_date_from = django_filters.DateFilter(
        field_name='payment_date',
        lookup_expr='gte'
    )
    payment_date_to = django_filters.DateFilter(
        field_name='payment_date',
        lookup_expr='lte'
    )

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']
