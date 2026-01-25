from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Course(models.Model):
    """Модель курса"""
    
    title = models.CharField(
        _('title'),
        max_length=255
    )
    
    preview = models.ImageField(
        _('preview'),
        upload_to='courses/previews/',
        blank=True,
        null=True
    )
    
    description = models.TextField(
        _('description')
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name=_('owner')
    )
    
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
    
    def __str__(self):
        return self.title

class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(
        _('title'),
        max_length=255
    )
    
    description = models.TextField(
        _('description')
    )
    
    preview = models.ImageField(
        _('preview'),
        upload_to='lessons/previews/',
        blank=True,
        null=True
    )
    
    video_link = models.URLField(
        _('video link')
    )
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name=_('course')
    )
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lessons',
        verbose_name=_('owner')
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('lesson')
        verbose_name_plural = _('lessons')
    
    def __str__(self):
        return f"{self.title} ({self.course.title})"
