from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from materials.models import Course, Lesson
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class LessonTestCase(TestCase):
    """
    Тесты для CRUD операций с уроками
    """
    
    def setUp(self):
        """
        Настройка тестовых данных
        """
        # Создаем пользователей
        self.user = User.objects.create(
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User',
            is_active=True
        )
        self.moderator = User.objects.create(
            email='moderator@example.com',
            password='modpassword123',
            first_name='Moderator',
            last_name='User',
            is_active=True
        )
        
        # Создаем группу модераторов и добавляем пользователя
        from django.contrib.auth.models import Group
        moderators_group, _ = Group.objects.get_or_create(name='moderators')
        self.moderator.groups.add(moderators_group)
        
        # Создаем курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            owner=self.user
        )
        
        # Создаем урок
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
            owner=self.user,
            video_url='https://www.youtube.com/watch?v=test123'  # Корректная YouTube ссылка
        )
        
        # Создаем клиенты API
        self.client = APIClient()
        self.moderator_client = APIClient()
        # Аутентифицируем клиентов
        self.client.force_authenticate(user=self.user)
        self.moderator_client.force_authenticate(user=self.moderator)
    
    def test_create_lesson_success(self):
        """
        Тест успешного создания урока
        """
        url = reverse('lesson-create')
        data = {
            'title': 'New Lesson',
            'description': 'New Lesson Description',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/watch?v=newvideo123'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.count(),
            2  # Один уже был создан в setUp
        )
        self.assertEqual(
            Lesson.objects.get(title='New Lesson').owner,
            self.user
        )
    def test_create_lesson_invalid_url(self):
        """
        Тест создания урока с некорректной ссылкой (не YouTube)
        """
        url = reverse('lesson-create')
        data = {
            'title': 'Invalid URL Lesson',
            'description': 'Lesson with invalid URL',
            'course': self.course.id,
            'video_url': 'https://vimeo.com/123456'  # Некорректная ссылка (не YouTube)
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn('video_url', response.data)
    
    def test_list_lessons(self):
        """
        Тест получения списка уроков
        """
        url = reverse('lesson-list')
        response = self.client.get(url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            len(response.data['results']),
            1  # Один урок создан в setUp
        )

    def test_retrieve_lesson(self):
        """
        Тест получения детальной информации об уроке
        """
        url = reverse('lesson-detail', args=[self.lesson.id])
        response = self.client.get(url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'],
            'Test Lesson'
        )
    
    def test_update_lesson_owner(self):
        """
        Тест обновления урока владельцем
        """
        url = reverse('lesson-update', args=[self.lesson.id])
        data = {
            'title': 'Updated Lesson Title',
            'description': 'Updated Description',
            'video_url': 'https://www.youtube.com/watch?v=updated123'
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.lesson.refresh_from_db()
        self.assertEqual(
            self.lesson.title,
            'Updated Lesson Title'
        )
    
    def test_update_lesson_moderator(self):
        """
        Тест обновления урока модератором
        """
        url = reverse('lesson-update', args=[self.lesson.id])
        data = {
            'title': 'Updated by Moderator',
            'description': 'Updated by moderator description'
        }
        
        response = self.moderator_client.patch(url, data)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.lesson.refresh_from_db()
        self.assertEqual(
            self.lesson.title,
            'Updated by Moderator'
        )
    
    def test_delete_lesson_owner(self):
        """
        Тест удаления урока владельцем
        """
        url = reverse('lesson-delete', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.count(),
            0
        )
    
    def test_delete_lesson_moderator_forbidden(self):
        """
        Тест запрета удаления урока модератором
        """
        url = reverse('lesson-delete', args=[self.lesson.id])
        response = self.moderator_client.delete(url)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            Lesson.objects.count(),
            1  # Урок все еще существует
        )
    
    def test_pagination(self):
        """
        Тест пагинации уроков
        """
        # Создаем дополнительные уроки для теста пагинации
        for i in range(15):
            Lesson.objects.create(
                title=f'Lesson {i}',
                description=f'Description {i}',
                course=self.course,
                owner=self.user,
                video_url=f'https://www.youtube.com/watch?v=test{i}'
            )
        url = reverse('lesson-list')
        response = self.client.get(url, {'page_size': 5})
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            len(response.data['results']),
            5  # Пагинация работает
        )
        self.assertIn(
            'total_pages',
            response.data
        )
        self.assertIn(
            'current_page',
            response.data
        )
    
    def test_lesson_validation_youtube_only(self):
        """
        Тест валидации YouTube ссылок
        """
        # Тест с корректной YouTube ссылкой
        lesson = Lesson(
            title='Valid YouTube',
            description='Test',
            course=self.course,
            owner=self.user,
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        lesson.full_clean()  # Не должно вызывать исключение
        
        # Тест с некорректной ссылкой (должно вызвать ValidationError)
        lesson.video_url = 'https://vimeo.com/123456'
        with self.assertRaises(Exception):
            lesson.full_clean()
        
        # Тест с youtu.be (сокращенная ссылка)
        lesson.video_url = 'https://youtu.be/dQw4w9WgXcQ'
        lesson.full_clean()  # Не должно вызывать исключение
    def test_lesson_description_validation(self):
        """
        Тест валидации ссылок в описании
        """
        # Описание с корректной YouTube ссылкой
        lesson = Lesson(
            title='Test',
            description='Смотрите видео: https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )
        lesson.full_clean()  # Не должно вызывать исключение
        
        # Описание с некорректной ссылкой
        lesson.description = 'Смотрите здесь: https://vimeo.com/123456'
        with self.assertRaises(Exception):
            lesson.full_clean()
