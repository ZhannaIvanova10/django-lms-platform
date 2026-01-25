from django.core.exceptions import ValidationError
from rest_framework import serializers
from urllib.parse import urlparse
import re


def validate_youtube_only(value):
    """
    Валидатор для проверки, что ссылка ведет только на youtube.com
    """
    if not value:
        return value
    
    # Проверяем, что это вообще ссылка
    try:
        parsed_url = urlparse(value)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValidationError("Некорректная ссылка")
        
        # Проверяем, что домен youtube.com
        domain = parsed_url.netloc.lower()
        # Разрешаем youtube.com и youtu.be (сокращенные ссылки)
        allowed_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'www.youtu.be']
        
        # Проверяем основной домен
        is_youtube = any(domain.endswith(allowed) for allowed in allowed_domains)
        
        # Также разрешаем субдомены youtube (например, m.youtube.com)
        if 'youtube.com' in domain or 'youtu.be' in domain:
            is_youtube = True
            
        if not is_youtube:
            raise ValidationError(
                "Разрешены только ссылки на YouTube. "
                f"Получена ссылка на: {parsed_url.netloc}"
            )
        
    except Exception as e:
        if isinstance(e, ValidationError):
            raise e
        raise ValidationError(f"Ошибка валидации ссылки: {str(e)}")
    
    return value

class YouTubeValidator:
    """
    Класс-валидатор для проверки YouTube ссылок
    """
    def __init__(self, field):
        self.field = field
    
    def __call__(self, attrs):
        value = attrs.get(self.field)
        return validate_youtube_only(value)


def validate_video_url(value):
    """
    Валидатор для поля video_url (только YouTube)
    """
    return validate_youtube_only(value)


def validate_description(value):
    """
    Валидатор для проверки ссылок в описании
    """
    if not value:
        return value
    
    # Ищем все ссылки в тексте
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, value)

    for url in urls:
        try:
            validate_youtube_only(url)
        except ValidationError as e:
            raise ValidationError(
                f"В описании найдена запрещенная ссылка: {url}. "
                "Разрешены только ссылки на YouTube."
            )
    
    return value
