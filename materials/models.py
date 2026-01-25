from django.db import models
from django.core.exceptions import ValidationError
from config import settings
from .validators import validate_youtube_only


NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='courses/previews/', verbose_name='Превью', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
    
    def clean(self):
        """
        Валидация на уровне модели
        """
        from .validators import validate_description
        if self.description:
            validate_description(self.description)
        super().clean()


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='lessons/previews/', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['-created_at']
    
    def clean(self):
        """
        Валидация на уровне модели
        """
        from .validators import validate_video_url, validate_description
        
        if self.video_url:
            validate_video_url(self.video_url)
        
        if self.description:
            validate_description(self.description)
        
        super().clean()
    
    def save(self, *args, **kwargs):
        """
        Переопределяем save для вызова clean
        """
        self.clean()
        super().save(*args, **kwargs)

class Subscription(models.Model):
    """
    Модель подписки пользователя на курс
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name='Пользователь',
        related_name='subscriptions'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        verbose_name='Курс',
        related_name='subscriptions'
    )
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'course']  # Один пользователь - одна подписка на курс
    
    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"
