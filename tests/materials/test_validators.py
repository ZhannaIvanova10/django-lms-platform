from django.test import TestCase
from django.core.exceptions import ValidationError
from materials.validators import validate_youtube_only


class ValidatorTests(TestCase):
    def test_valid_youtube_url(self):
        """Проверка валидных YouTube ссылок"""
        valid_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtu.be/dQw4w9WgXcQ',
            'https://www.youtube.com/embed/dQw4w9WgXcQ',
            'http://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtube.com/watch?v=dQw4w9WgXcQ',
        ]
        
        for url in valid_urls:
            try:
                validate_youtube_only(url)
            except ValidationError:
                self.fail(f"Valid URL failed validation: {url}")
    
    def test_invalid_youtube_url(self):
        """Проверка невалидных ссылок"""
        invalid_urls = [
            'https://vimeo.com/123456',
            'https://example.com/video',
            'https://rutube.ru/video/123',
            'not-a-url',
            '',
            None,
        ]
        
        for url in invalid_urls:
            if url is not None:
                with self.assertRaises(ValidationError):
                    validate_youtube_only(url)
