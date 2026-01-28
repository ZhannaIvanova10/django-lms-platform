from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from materials.models import Course, Lesson

User = get_user_model()


class LessonCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.moderator = User.objects.create_user(
            email='moderator@example.com',
            password='testpass123',
            first_name='Moderator',
            last_name='User',
            is_staff=True
        )
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Course Description',
            owner=self.user
        )
        
        self.lesson_data = {
            'title': 'Test Lesson',
            'description': 'Lesson Description',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'course': self.course.id,
            'order': 1
        }
    
    def test_create_lesson_as_owner(self):
        """Владелец может создавать уроки"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/lessons/create/', self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
    def test_create_lesson_as_moderator_fails(self):
        """Модератор не может создавать уроки"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post('/api/lessons/create/', self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_lessons(self):
        """Получение списка уроков"""
        Lesson.objects.create(
            title='Test Lesson',
            course=self.course,
            owner=self.user,
            video_url='https://www.youtube.com/watch?v=test'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_retrieve_lesson(self):
        """Получение конкретного урока"""
        lesson = Lesson.objects.create(
            title='Test Lesson',
            course=self.course,
            owner=self.user,
            video_url='https://www.youtube.com/watch?v=test'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Lesson')
    
    def test_update_lesson_as_owner(self):
        """Владелец может обновлять урок"""
        lesson = Lesson.objects.create(
            title='Old Title',
            course=self.course,
            owner=self.user,
            video_url='https://www.youtube.com/watch?v=test'
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f'/api/lessons/{lesson.id}/update/',
            {'title': 'New Title'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, 'New Title')
    
    def test_delete_lesson_as_owner(self):
        """Владелец может удалять урок"""
        lesson = Lesson.objects.create(
            title='Test Lesson',
            course=self.course,
            owner=self.user,
            video_url='https://www.youtube.com/watch?v=test'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/lessons/{lesson.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
    
    def test_youtube_url_validation(self):
        """Проверка валидации YouTube ссылок"""
        self.client.force_authenticate(user=self.user)
        
        # Невалидная ссылка (не YouTube)
        invalid_data = self.lesson_data.copy()
        invalid_data['video_url'] = 'https://vimeo.com/123456'
        
        response = self.client.post('/api/lessons/create/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', response.data)
