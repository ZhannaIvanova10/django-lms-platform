from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

def validate_youtube_only(value):
    """Валидатор для проверки YouTube ссылок."""
    if not value:
        return
    
    youtube_patterns = [
        r'^https?://(www\.)?youtube\.com/',
        r'^https?://youtu\.be/',
        r'^https?://(www\.)?youtube\.com/embed/',
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, value):
            return
    
    raise ValidationError('Допускаются только ссылки на YouTube.')

class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    video_url = models.URLField(
        verbose_name='Ссылка на видео',
        validators=[validate_youtube_only]
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
