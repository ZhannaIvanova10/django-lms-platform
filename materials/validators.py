from django.core.exceptions import ValidationError
import re

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
