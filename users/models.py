from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User с email вместо username"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email обязателен'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Кастомная модель пользователя"""
    
    username = None  # Убираем username
    
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    phone = models.CharField(
        _('phone number'),
        max_length=15,
        blank=True,
        null=True
    )
    
    city = models.CharField(
        _('city'),
        max_length=100,
        blank=True,
        null=True
    )
    
    avatar = models.ImageField(
        _('avatar'),
        upload_to='users/avatars/',
        blank=True,
        null=True
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email

class Payment(models.Model):
    """Модель платежа (Задание 2)"""
    
    # Способы оплаты
    CASH = 'cash'
    TRANSFER = 'transfer'
    
    PAYMENT_METHODS = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод на счет'),
    ]
    
    # Связи
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='пользователь'
    )
    
    course = models.ForeignKey(
        'materials.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='оплаченный курс'
    )
    lesson = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='оплаченный урок'
    )
    
    # Поля
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата оплаты'
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='сумма оплаты'
    )
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name='способ оплаты'
    )
    
    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-payment_date']
    
    def __str__(self):
        if self.course:
            return f"{self.user.email} - {self.course.title} - {self.amount}"
        elif self.lesson:
            return f"{self.user.email} - {self.lesson.title} - {self.amount}"
        else:
            return f"{self.user.email} - {self.amount}"
    def clean(self):
        """Проверка: либо курс, либо урок должен быть указан"""
        from django.core.exceptions import ValidationError
        
        if not self.course and not self.lesson:
            raise ValidationError("Должен быть указан либо курс, либо урок")
        
        if self.course and self.lesson:
            raise ValidationError("Можно указать только либо курс, либо урок")
