from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from materials.models import Course, Lesson


class Payment(models.Model):
    """Модель платежа"""
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('user')
    )
    payment_date = models.DateTimeField(_('payment date'), auto_now_add=True)
    
    # Один платеж может быть либо за курс, либо за урок
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name=_('paid course')
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name=_('paid lesson')
    )
    
    amount = models.DecimalField(
        _('amount'),
        max_digits=10,
        decimal_places=2
    )
    payment_method = models.CharField(
        _('payment method'),
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )
    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        ordering = ['-payment_date']
    
    def __str__(self):
        item = self.paid_course or self.paid_lesson
        return f"{self.user.email} - {item} - {self.amount}"
    
    def clean(self):
        """Проверяем, что указан либо курс, либо урок"""
        from django.core.exceptions import ValidationError
        
        if not self.paid_course and not self.paid_lesson:
            raise ValidationError('Должен быть указан либо курс, либо урок')
        if self.paid_course and self.paid_lesson:
            raise ValidationError('Можно указать либо курс, либо урок, но не оба сразу')
